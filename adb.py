# -*- coding: utf-8 -*-
import os, subprocess, re

platform_tools = os.path.join(__file__, 'platform-tools') 
platform_tools = platform_tools if os.path.exists(platform_tools) else ''

def execute(command, wait = True):
    process = subprocess.Popen(
        'adb' + ' ' + command, 
        shell = True, 
        stdout = subprocess.PIPE,
        cwd = platform_tools if platform_tools else None
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