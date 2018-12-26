# -*- coding: utf-8 -*-
import os, subprocess, re

WORKDIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_PATH = os.path.join(WORKDIR, 'platform-tools')

def execute(command, wait = True):
    process = subprocess.Popen(
        'adb' + ' ' + command, 
        shell = True, 
        stdout = subprocess.PIPE,
        cwd = TOOLS_PATH if os.path.exists(TOOLS_PATH) else None
    )
    if wait: process.wait()
    return process

def read(command, encode = True):
    data = execute(command, wait = False).stdout.read()
    return data.decode('utf-8') if encode else data

def connect():
    if re.search(r'device\s+$', read('devices')):
        return True
    else:
        execute('kill-server')
        return False