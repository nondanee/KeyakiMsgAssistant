# -*- coding: utf-8 -*-
import os, subprocess, re

portable_adb = './platform-tools' if os.path.exists('./platform-tools') else None

def execute(command, wait = True):
    process = subprocess.Popen(
        'adb' + ' ' + command, 
        shell = True, 
        stdout = subprocess.PIPE,
        cwd = portable_adb if portable_adb else None
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