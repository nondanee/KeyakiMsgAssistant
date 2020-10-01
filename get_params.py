# -*- coding: utf-8 -*-
import xml.dom.minidom, base64, json, os
from Crypto.Cipher import AES
from common import ADB, PARAMS_PATH

def extract(string):
    document = xml.dom.minidom.parseString(string)
    collection = document.documentElement
    for node in collection.getElementsByTagName('string'):
        if node.getAttribute('name') == 'AUTHORIZATION':
            authorization_encrypted = base64.b64decode(node.childNodes[0].nodeValue)
            return authorization_encrypted

def shuffle(string):
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

adb = ADB()

file_00 = adb.read('''shell "su -c 'base64 /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_00'"''', encode = False)
file_01 = adb.read('''shell "su -c 'base64 /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_01'"''', encode = False)
hot_preference = adb.read('''shell "su -c 'cat /data/data/jp.co.sonymusic.communication.keyakizaka/shared_prefs/hot_preference.xml'"''')

product_model = adb.read('shell getprop ro.product.model').strip()
build_version = adb.read('shell getprop ro.build.version.release').strip()
build_id = adb.read('shell getprop ro.build.id').strip()

adb.kill()

try:
    file_00 = base64.b64decode(file_00)
    try: file_01 = base64.b64decode(file_01)
    except: pass
    if not file_01: file_01 = file_00[16:]
    iv = file_00[0:16]
    key = shuffle(file_01)
    authorization_encrypted = extract(hot_preference)
    authorization = json.loads(decrypt(key, iv, authorization_encrypted))
    user_agent = 'Dalvik/2.1.0 (Linux; U; Android {build_version}; {product_model} Build/{build_id})'.format(
        build_version = build_version if build_version else '6.0',
        product_model = product_model if product_model else 'Nexus 5',
        build_id = build_id if build_id else 'MRA58N'
    )

    print('authorization', authorization)
    print('user-agent', user_agent)

    try:
        with open(PARAMS_PATH, 'r') as f:
            params = json.loads(f.read())
    except:
        params = {}
    
    params['authorization'] = authorization
    params['user_agent'] = user_agent
    params['app_id'] = 'jp.co.sonymusic.communication.keyakizaka 2.0'

    with open(PARAMS_PATH, 'w') as f:
        f.write(json.dumps(params, indent = 4))
        

except Exception as e:
    print('error', e)
else:
    print('success')
finally:
    os.system('pause')