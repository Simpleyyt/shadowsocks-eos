# coding: utf-8
import os
from subprocess import Popen, call

def stop():
    # hahaha~~~
    for i in range(0, 20):
        os.system('killall ss-local 2> /dev/null')

def start(host, port, password, method, local_port):
    stop()
    Popen (['ss-local',
           '-s', host,
           '-p', str(port),
           '-l', str(local_port),
           '-k', password,
           '-m', method,
           '-v'])
