# coding: utf-8
import os
from subprocess import Popen, call
from config import Config

def stop():
  call(['sslocal',
        '-s', '127.0.0.1',
        '-d', 'stop',
        '--pid-file', Config.path + '.pid'])

def start(host, port, password, method, local_port):
    stop()
    call(['sslocal',
          '-s', host,
          '-p', str(port),
          '-l', str(local_port),
          '-k', password,
          '-m', method,
          '-d', 'start',
          '--log-file', Config.path + '.log',
          '--pid-file', Config.path + '.pid'])
