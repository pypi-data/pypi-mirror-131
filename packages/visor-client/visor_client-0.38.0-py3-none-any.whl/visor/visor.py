#!/usr/bin/python3.8

import argparse
import base64
import binascii
import blake3
import datetime
import dockerfile
import fasteners
import hashlib
import io
import json
import multiprocessing
import os
import paramiko
import requests
import shlex
import shutil
import sseclient
import subprocess
import sys
import tempfile
import time

from fastcdc import fastcdc
from pathlib import Path
from stat import ST_MODE
from urllib.parse import urlparse

VISOR_DIR = os.path.expanduser('~/.visor')
VISOR_CONFIG = os.path.join(VISOR_DIR, 'config.json')

# TODO: make ctrl+c properly cancel a build
# TODO: partition by team
# TODO: should be able to `visor console <container_id>` to recover from broken ssh
# TODO: REPEATABLE should be taking state of all required machines not just cur
# TODO: SNAPSHOT should be global/local to a machine
# TODO: total time getting printed before error
# TODO: clean up network after all containers in that network are gone
# TODO: host CPU going crazy even when guest cpu is close to idle
# TODO: server should be able to specify root dir instead of ~/.visorserver

def run_as_process(func, *args):
  queue = multiprocessing.Queue()

  def wrap_for_subprocess(func, *args):
    queue.put(func(*args))

  p = multiprocessing.Process(target=wrap_for_subprocess, args=[func, *args])

  try:
    p.start()
    while queue.empty():
      if not p.is_alive():
        exit(1)
      time.sleep(0.1)
    ret = queue.get()
    p.join()
  finally:
    p.terminate()
  queue.close()
  return ret

config = {}
if os.path.exists(VISOR_CONFIG):
  with open(VISOR_CONFIG, 'r') as f:
    config = json.loads(f.read())

def get_hash(string):
  return hashlib.sha256(string.encode('utf8')).hexdigest()[:30]

def get_command_value(command):
  return command.original[len(command.cmd):].strip()

def validate_server_url(server_url=None):
  if not server_url:
    if 'defaultServer' not in config:
      raise Exception('You need to run `visor login` first')
    return config['defaultServer']
  return server_url

def _api_call(*args, **kwargs):
  if 'timeout' not in kwargs:
    kwargs['timeout'] = 120
  server_url = validate_server_url(kwargs.get('server_url'))
  if 'server_url' in kwargs:
    del kwargs['server_url']
  if len(args) >= 2:
    args = list(args)
    args[1] = server_url + '/api/v1/' + args[1]
  if 'url' in kwargs:
    kwargs['url'] = server_url + '/api/v1/' + kwargs['url']
  return requests.request(*args, **kwargs)

exitcode = 0
def _stream(resp):
  global exitcode
  client = sseclient.SSEClient(resp)
  for event in client.events():
    if event.event == 'log':
      print(json.loads(event.data), end='')
    elif event.event == 'error':
      print(json.loads(event.data))
      exitcode = 1
    else:
      print(event)
      raise Exception(f'Unknown event type {event.event}')

def safe_non_stream_api_call(*args, **kwargs):
  resp = _api_call(*args, **kwargs)
  if resp.status_code == 200:
    return resp.json()
  raise Exception('Server responded with %s: %s' % (resp.status_code, resp.text))

def safe_stream_api_call(*args, **kwargs):
  kwargs['stream'] = True
  if 'timeout' not in kwargs:
    kwargs['timeout'] = 3600
  resp = _api_call(*args, **kwargs)
  if resp.status_code == 200:
    return _stream(resp)
  raise Exception('Server responded with %s; %s' % (resp.status_code, resp.text))

def verify_login(server_url=None):
  if not server_url:
    if 'defaultServer' not in config:
      raise Exception('You need to run `visor login` first')
    server_url = config['defaultServer']
  if server_url not in config['auths']:
    raise Exception('You are not logged into server %s' % server_url)
  return server_url

def do_login(args):
  if not args.url.startswith('http'):
    raise argparse.ArgumentTypeError('url must start with http or https')
  resp = safe_non_stream_api_call(
    'post',
    'login',
    json={'username': args.username, 'password': args.password},
    server_url=args.url
  )
  if 'auths' not in config:
    config['auths'] = {}
  if args.url not in config['auths']:
    config['auths'][args.url] = {}
  config['auths'][args.url]['username'] = args.username
  config['auths'][args.url]['sshHost'] = urlparse(args.url).hostname
  config['auths'][args.url]['sshPort'] = resp['sshPort']
  config['auths'][args.url]['sshUsername'] = resp['username']
  config['auths'][args.url]['sshKey'] = resp['key']
  config['defaultServer'] = args.url
  os.makedirs(VISOR_DIR, exist_ok=True)
  with open(VISOR_CONFIG, 'w') as f:
    f.write(json.dumps(config, indent=2))

def find_context_dir(visorfile):
  ret = os.path.dirname(os.path.abspath(visorfile))
  cur = ret
  while cur != os.path.dirname(cur):
    if os.path.exists(os.path.join(cur, '.git')):
      return cur
    cur = os.path.dirname(cur)
  return ret

def add_all_files_and_subfiles(context_dir, files, path):
  if os.path.isdir(path):
    for root, dirs, fs in os.walk(path):
      for f in fs:
        name = os.path.abspath(os.path.join(root, f))
        if os.path.commonpath([name, context_dir]) != context_dir:
          raise Exception(f'Illegal COPY {name}')
        files.add(name)
      for d in dirs:
        name = os.path.abspath(os.path.join(root, d))
        if os.path.commonpath([name, context_dir]) != context_dir:
          raise Exception(f'Illegal COPY {name}')
        if os.path.islink(name):
          files.add(name)
  else:
    name = os.path.abspath(path)
    if os.path.commonpath([name, context_dir]) != context_dir:
      raise Exception(f'Illegal COPY {name}')
    files.add(name)

def find_context_files(visorfile):
  visorfile = os.path.abspath(visorfile)
  context_dir = find_context_dir(visorfile)
  cur_visorfile = visorfile
  files = {visorfile}
  for i in range(10):
    next_visorfile = None
    visorfile_dir = os.path.dirname(cur_visorfile)
    with open(cur_visorfile, 'r') as f:
      commands = dockerfile.parse_string(f.read())
      for command in commands:
        if command.cmd == 'inherit':
          base = get_command_value(command)
          if base.startswith('.'):
            next_visorfile = os.path.join(visorfile_dir, base)
            if os.path.isdir(next_visorfile):
              next_visorfile = os.path.join(next_visorfile, 'Visorfile')
            if os.path.commonpath([next_visorfile, context_dir]) != context_dir:
              raise Exception(f'Illegal INHERIT {base}')
            files.add(next_visorfile)
        elif command.cmd == 'copy':
          # TOOD escaped spaces won't work
          paths = get_command_value(command).split(' ')
          host_paths = paths[:-1]
          for host_path in host_paths:
            if host_path.startswith('/'):
              add_all_files_and_subfiles(
                context_dir, files, os.path.join(context_dir, host_path)
              )
            else:
              add_all_files_and_subfiles(
                context_dir, files, os.path.join(visorfile_dir, host_path)
              )
        elif command.cmd == 'repeatable':
          values = get_command_value(command).split(' ')
          if len(values) == 3 and values[0].lower() == 'script':
            if values[2].startswith('/'):
              add_all_files_and_subfiles(
                context_dir, files, os.path.join(context_dir, values[2])
              )
            else:
              add_all_files_and_subfiles(
                context_dir, files, os.path.join(visorfile_dir, values[2])
              )
    if not next_visorfile:
      break
    cur_visorfile = next_visorfile
  else:
    raise Exception('FROM chain is too long')
  if os.path.exists(os.path.join(context_dir, '.git')):
    ignored = subprocess.check_output([
      'git', 'ls-files', '-o', '-i', '--exclude-standard'
    ], cwd=context_dir).decode('utf8').splitlines()
    # get all ignored files, recursively for all submodules, and write
    # paths rooted at the context_dir
    # HACK: need the command above separately because this call does not
    # include a call to the root repo
    ignored.extend(subprocess.check_output([
      'git', 'submodule', 'foreach', '--recursive',
      'git ls-files -o -i --exclude-standard | sed "s|^|$path/|"',
    ], cwd=context_dir).decode('utf8').splitlines())
    ignored = set([
      os.path.normpath(os.path.join(context_dir, x)) for x in ignored
    ])
    files = {os.path.normpath(x) for x in files}
    files = {x for x in files if x not in ignored}

  files = [os.path.relpath(x, start=context_dir) for x in files]
  return files

# TODO: Using small json names in order to minimize transport size. Use a
# binary transport instead so the code remains readable
# t - type
# v - value
# p - permissions
def create_mapped_file(context_dir, filemap, context_relative_path):
  parts = Path(context_relative_path).parts
  curpath = context_dir
  for part in parts[:-1]:
    curpath = os.path.join(curpath, part)
    if part in filemap:
      filemap = filemap[part]['v']
      continue
    filemap[part] = {
      't': 'd',
      'v': {},
      'p': os.stat(curpath)[ST_MODE]
    }
    filemap = filemap[part]['v']
  filemap[parts[-1]] = {}
  return filemap[parts[-1]]

def chunkify(context_dir, files):
  chunks = {}
  filemap = {
    't': 'd',
    'v': {},
  }
  for f in files:
    abs_file = os.path.join(context_dir, f)
    if os.path.islink(abs_file):
      mapped_file = create_mapped_file(context_dir, filemap['v'], f)
      mapped_file['t'] = 'l'
      mapped_file['v'] = os.readlink(abs_file)
      # Symlink does not have its own permissions, permissions of target
      # are used instead
      continue
    if os.path.isdir(abs_file):
      raise Exception(f'Transmitting directories not supported {f}')
    mapped_file = create_mapped_file(context_dir, filemap['v'], f)
    mapped_file['t'] = 'f'
    mapped_file['v'] = []
    mapped_file['p'] = os.stat(abs_file)[ST_MODE]
    for chunk in fastcdc(abs_file, 2**11, 2**14, 2**15, hf=blake3.blake3, fat=True):
      mapped_file['v'].append(chunk.hash)
      chunks[chunk.hash] = chunk.data
  return filemap, chunks

def subprocess_transmit_context(visorfile):
  files = find_context_files(visorfile)
  context_dir = find_context_dir(visorfile)
  filemap, chunks = chunkify(context_dir, files)
  missing_chunks = safe_non_stream_api_call(
    'post', 'transmitmeta', json={'filemap': filemap}
  )['missing']
  MAX_CHUNKS_PER_UPLOAD = 1000
  for i in range(0, len(missing_chunks), MAX_CHUNKS_PER_UPLOAD):
    safe_non_stream_api_call(
      'post',
      'transmit',
      json={
        'chunks': {
          x: base64.b64encode(chunks[x]).decode('ascii') for x in
              missing_chunks[i:i + MAX_CHUNKS_PER_UPLOAD]
        }
      }
    )
  return filemap

def transmit_context(visorfile):
  # HACK: This part of the code needs to keep "fat" cdc chunks in memory.
  # In the worst case, this is the size of the entire repository being uploaded.
  # This can cause OOM if we have many clients run at nearly the same time,
  # such as starting multiple runs from a ci process.
  # In order to prevent this, we have a global lock on uploads that ends with
  # a forced garbage collect of the chunks. However, python's garbage collector
  # does not work as expected in this case. So to get around this, we put the
  # chunk processing in a subprocess (the chunks are freed when the subprocess
  # exits.
  # In most cases this lock is held for less than a second.
  # If uploading a large repository for the first time,
  # it will be held for the duration of the upload.
  with fasteners.InterProcessLock('/var/lock/visor-client-upload.lock'):
    return run_as_process(subprocess_transmit_context, visorfile)

def do_build_base(args):
  safe_stream_api_call(
    'post',
    'build_base',
    json={
      'os': args.os,
    },
  )

def send_streaming_command(args, command, json_data):
  print('Sending build context...')
  server_url = verify_login()
  visorfile = args.visorfile
  if os.path.isdir(visorfile):
    visorfile = os.path.join(visorfile, 'Visorfile')
  filemap = transmit_context(visorfile)
  print('Done sending build context\n')

  buildenvs = {}
  for x in args.buildenvs:
    a, b = x.split('=', 1)
    buildenvs[a] = b

  context_dir = find_context_dir(visorfile)
  json_data.update({
      'visorfileRelpath': os.path.relpath(visorfile, start=context_dir),
      'buildenvs': buildenvs,
      # TODO: transmitting the filemap once here and once above in the
      # transmitmeta. Could keep something on the server so we only have to
      # transmit once. The file metadata can get pretty big for lots of files.
      'filemap': filemap,
  })

  safe_stream_api_call(
    'post',
    command,
    json=json_data,
  )


def do_build(args):
  if not args.snapshot_on_failure:
    args.snapshot_on_failure = []
  for subargs in args.snapshot_on_failure:
    subargs[1] = int(subargs[1])
  send_streaming_command(args, 'build', {
    'keepRunning': args.keep_running,
    'snapshotOnFailure': args.snapshot_on_failure,
  })


def do_multirun(args):
  send_streaming_command(args, 'multirun', {
    'numRuns': args.num,
    'passString': args.pass_string,
    'failString': args.fail_string,
  })


def do_log(args):
  resp = _api_call('get', f'result/{args.multirun_id}?run={args.run_num}')
  if resp.status_code == 200:
    print(resp.text)
    return
    # return resp.json()
  raise Exception('Server responded with %s: %s' % (resp.status_code, resp.text))
  # print(safe_non_stream_api_call())

def do_run(args):
  resp = safe_non_stream_api_call(
    'post', 'run', json={'imageId': args.image_id}, timeout=600
  )
  print(resp['containerId'])

def do_ssh(args, server_url=None):
  guest_ssh_args = safe_non_stream_api_call(
    'get', 'guest_ssh_args', json={'containerId': args.container_id}
  )
  server_url = verify_login(server_url)
  c = config['auths'][server_url]
  with tempfile.NamedTemporaryFile('w', delete=True) as f:
    f.write(c['sshKey'])
    f.flush()
    subcmd = 'ssh -t -p %s -i %s -o "StrictHostKeyChecking no" %s@localhost %s' % (
      str(guest_ssh_args['port']),
      guest_ssh_args['keyFile'],
      guest_ssh_args['username'],
      shlex.quote(args.cmd) if args.cmd else ''
    )
    cmd = [x for x in [
      'ssh',
      '-t',
      '-p', str(c['sshPort']),
      '-i', f.name,
      '-o', 'StrictHostKeyChecking no',
      '%s@%s' % (c['sshUsername'], c['sshHost']),
      subcmd
    ] if x]
    os.execvp('ssh', cmd)

def do_console(args, server_url=None):
  guest_console_args = safe_non_stream_api_call(
    'get', 'guest_console_args', json={'containerId': args.container_id}
  )
  server_url = verify_login(server_url)
  c = config['auths'][server_url]
  with tempfile.NamedTemporaryFile('w', delete=True) as f:
    f.write(c['sshKey'])
    f.flush()
    subcmd = 'telnet localhost {port}'
    # TODO: LOH not sure how to make telnet secure

def do_throttle(args):
  json_to_send = {
    'containerId': args.container_id
  }
  if args.disk_bps is not None:
    json_to_send['diskBps'] = args.disk_bps
  if args.disk_iops is not None:
    json_to_send['diskIops'] = args.disk_iops
  resp = safe_non_stream_api_call('post', 'throttle', json=json_to_send)

def do_ps(args):
  resp = safe_non_stream_api_call('get', 'ps')
  if args.quiet:
    for container in resp['containers']:
      print(container['id'])
  else:
    print(f'{"CONTAINER ID":<35}', end='')
    print(f'{"MACHINE ID":<15}', end='')
    print(f'{"NETWORK ID":<15}', end='')
    print(f'{"STATUS":<10}', end='')
    print(f'{"STARTED":<15}', end='')
    print('')
    for container in resp['containers']:
      print(f'{container["id"]:<35}', end='')
      print(f'{container["machineId"]:<15}', end='')
      print(f'{container["networkId"]:<15}', end='')
      print(f'{container["status"]:<10}', end='')
      print(f'{container["birth"]:<15}', end='')
      print('')

def do_pause(args):
  resp = safe_non_stream_api_call(
    'post', 'pause', json={'containerId': args.container_id}
  )
  print(resp['containerId'])

def do_unpause(args):
  resp = safe_non_stream_api_call(
    'post', 'unpause', json={'containerId': args.container_id}
  )
  print(resp['containerId'])

def do_rm(args):
  resp = safe_non_stream_api_call(
    'post', 'rm', json={'containerId': args.container_id}
  )
  print(resp['containerId'])

def do_images(args):
  resp = safe_non_stream_api_call('get', 'images')
  for image in resp['images']:
    print(image)

def do_rmi(args):
  resp = safe_non_stream_api_call(
    'post', 'rmi', json={'imageId': args.image_id}
  )
  print(resp['imageId'])

def do_wipe(args):
  safe_stream_api_call(
    'post',
    'wipe',
    json={
      'includeBases': args.include_bases,
    },
  )

class Unbuffered(object):
  def __init__(self, stream):
    self.stream = stream
  def write(self, data):
    self.stream.write(data)
    self.stream.flush()
  def writelines(self, datas):
    self.stream.writelines(datas)
    self.stream.flush()
  def __getattr__(self, attr):
    return getattr(self.stream, attr)

def main():
  sys.stdout = Unbuffered(sys.stdout)

  main_parser = argparse.ArgumentParser(description='Visor client')
  subparsers = main_parser.add_subparsers(dest='subparser')
  subparsers.required = True

  login_parser = subparsers.add_parser('login', help='Log into a visor server')
  login_parser.add_argument('url')
  login_parser.add_argument('username')
  login_parser.add_argument('password')
  login_parser.set_defaults(func=do_login)

  build_base_parser = subparsers.add_parser(
    'build-base', help='Build a base image'
  )
  build_base_parser.add_argument(
    'os', choices=['ubuntu16', 'ubuntu18', 'ubuntu20']
  )
  build_base_parser.set_defaults(func=do_build_base)

  build_parser = subparsers.add_parser('build', help='Build a Visorfile')
  build_parser.add_argument('--keep-running', action='store_true')
  build_parser.add_argument(
    '--snapshot-on-failure',
    action='append',
    nargs=3,
    metavar=('failure_string', 'max_snapshot_rate_in_minutes', 'note_string'),
    help='''
      Takes 3 arguments.
      The first argument is a failure string to match for. Snapshots will only
      be taken after a failure if the failing command contains this string.
      The second argument is a number representing how many minutes to wait
      since the last time a snapshot of the same failure string was taken.
      Set to 0 if you want to always take snapshots of the given failure string.
      The third argument is a note which you can use to store arbitrary metadata
      about the snapshot.
    '''
  )
  build_parser.add_argument('--build-env', dest='buildenvs', action='append', default=[])
  build_parser.add_argument('visorfile', help='The Visorfile to build')
  build_parser.set_defaults(func=do_build)

  multirun_parser = subparsers.add_parser('multirun', help='Build a Visorfile multiple time')
  multirun_parser.add_argument('--build-env', dest='buildenvs', action='append', default=[])
  multirun_parser.add_argument('visorfile', help='The Visorfile to build')
  multirun_parser.add_argument('num', type=int, default=10, help='The number of time the visorfile needs to be run')
  multirun_parser.add_argument('--pass-string', type=str, default='', help='The string to search for pass status')
  multirun_parser.add_argument('--fail-string', type=str, default='', help='The string to search for fail status')
  multirun_parser.set_defaults(func=do_multirun)

  log_parser = subparsers.add_parser('log', help='Download a log from multiplerun command')
  log_parser.add_argument('multirun_id', type=str, help='The id of the multirun')
  log_parser.add_argument('run_num', type=str, nargs="?", default="", help='The run number of the log')
  log_parser.set_defaults(func=do_log)

  run_parser = subparsers.add_parser('run', help='Run an instance of image_id')
  run_parser.add_argument('image_id', type=str)
  run_parser.set_defaults(func=do_run)

  ssh_parser = subparsers.add_parser('ssh', help='SSH to a running container')
  ssh_parser.add_argument('container_id', type=str)
  ssh_parser.add_argument('cmd', type=str, nargs='?', default=None)
  ssh_parser.set_defaults(func=do_ssh)

  console_parser = subparsers.add_parser(
    'console', help='Display the console to a running container'
  )
  console_parser.add_argument('container_id', type=str)
  console_parser.set_defaults(func=do_console)

  throttle_parser = subparsers.add_parser(
    'throttle', help='Throttle the disk of a running container'
  )
  throttle_parser.add_argument('container_id', type=str)
  throttle_parser.add_argument('--disk-bps', type=int)
  throttle_parser.add_argument('--disk-iops', type=int)
  throttle_parser.set_defaults(func=do_throttle)

  ps_parser = subparsers.add_parser('ps', help='List running containers')
  ps_parser.add_argument('--quiet', '-q', action='store_true')
  ps_parser.set_defaults(func=do_ps)

  unpause_parser = subparsers.add_parser('unpause', help='Start a running container')
  unpause_parser.add_argument('container_id', type=str)
  unpause_parser.set_defaults(func=do_unpause)

  pause_parser = subparsers.add_parser('pause', help='Pause a running container')
  pause_parser.add_argument('container_id', type=str)
  pause_parser.set_defaults(func=do_pause)

  rm_parser = subparsers.add_parser('rm', help='Kill a container')
  rm_parser.add_argument('container_id', type=str)
  rm_parser.add_argument('--force', type=bool, default=False)
  rm_parser.set_defaults(func=do_rm)

  images_parser = subparsers.add_parser('images', help='List all images')
  images_parser.set_defaults(func=do_images)

  rmi_parser = subparsers.add_parser('rmi', help='Delete an image')
  rmi_parser.add_argument('image_id', type=str)
  rmi_parser.set_defaults(func=do_rmi)

  wipe_parser = subparsers.add_parser('wipe', help='Wipe all images and vms')
  wipe_parser.add_argument('--include-bases', action='store_true')
  wipe_parser.set_defaults(func=do_wipe)

  args = main_parser.parse_args()
  args.func(args)

  sys.exit(exitcode)

if __name__ == '__main__':
  main()
