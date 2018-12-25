# -*- coding: utf-8 -*-
import os, sys, platform, subprocess
import xml.dom.minidom, base64, re, json
import adb
from Crypto.Cipher import AES

def extract(string):
    document = xml.dom.minidom.parseString(string)
    collection = document.documentElement
    for node in collection.getElementsByTagName('string'):
        if node.getAttribute('name') == 'ACCOUNT_ID':
            account_id_encrypted = base64.b64decode(node.childNodes[0].nodeValue)
        if node.getAttribute('name') == 'AUTH_TOKEN':
            auth_token_encrypted = base64.b64decode(node.childNodes[0].nodeValue)
    return account_id_encrypted, auth_token_encrypted

def permutate(string):
    byte_array = bytearray(string)
    for i, _ in enumerate(byte_array):
        temp = byte_array[i]
        if i % 2 == 0:
            j = temp & 0xC
            k = temp & 0x3
            temp = temp & 0xF0
            temp = (j >> 2) + temp
            temp = temp + (k << 2)
            byte_array[i] = temp
    return bytes(byte_array)

def decrypt(key, iv, cipher_text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(cipher_text).rstrip().decode()


if adb.connect():
    print('connect')
else:
    print("can't connect to device")
    os.system('pause')
    exit()

file_00 = adb.read('''shell "su -c 'cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_00'"''', encode = False)
file_01 = adb.read('''shell "su -c 'cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_01'"''', encode = False)
hot_preference = adb.read('''shell "su -c 'cat /data/data/jp.co.sonymusic.communication.keyakizaka/shared_prefs/hot_preference.xml'"''')

product_model = adb.read('shell getprop ro.product.model').strip()
build_version = adb.read('shell getprop ro.build.version.release').strip()
build_id = adb.read('shell getprop ro.build.id').strip()
adb.execute('kill-server')

try:
    iv = file_00
    key = permutate(file_01)
    account_id_encrypted, auth_token_encrypted = extract(hot_preference)
    account_id = decrypt(key, iv, account_id_encrypted)
    auth_token = decrypt(key, iv, auth_token_encrypted)
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android {build_version}; {product_model} Build/{build_id})'.format(
        build_version = build_version if build_version else '6.0',
        product_model = product_model if product_model else 'Nexus 5',
        build_id = build_id if build_id else 'MRA58N'
    )

    print('account-id', account_id)
    print('auth-token', auth_token)
    print('user-agent', user_agent)

    with open('./params.json', 'w') as params_file:
        params_file.write(
            json.dumps({
                'account_id': account_id,
                'auth_token': auth_token,
                'user_agent': user_agent,
                'api_version': '1.4.0'
            }, indent = 4)
        )
except Exception as e:
    print('error', e)
else:
    print('success')
finally:
    os.system('pause')