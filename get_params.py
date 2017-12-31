# -*- coding: utf-8 -*-
import os, sys
import xml.dom.minidom, base64
from Crypto.Cipher import AES
import re, json

if getattr(sys, 'frozen', False):
    work_dir = os.path.dirname(sys.executable)
else:
    work_dir = os.path.dirname(__file__)

adb_dir = os.path.join(work_dir,"platform-tools") if os.path.exists("platform-tools") else ""
adb = os.path.join(adb_dir,"adb") + " "
params_path = os.path.join(work_dir,"params.json")

connect = os.popen(adb + "devices").read()
if re.search(r"device\s+$",connect) == None:
    print "can't connect to device"
    os.system(adb + "kill-server")
    sys.stdin.read()
    exit()
else:
    print "connect"

file_00 = os.popen(adb + 'shell "su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_00"').read()
file_01 = os.popen(adb + 'shell "su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_01"').read()
hot_preference = os.popen(adb + 'shell "su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/shared_prefs/hot_preference.xml"').read()

product_model = os.popen(adb + "shell getprop ro.product.model").read()
product_model = re.sub(r"[\r\n]","",product_model)
build_version = os.popen(adb + "shell getprop ro.build.version.release").read()
build_version = re.sub(r"[\r\n]","",build_version)
build_id = os.popen(adb + "shell getprop ro.build.id").read()
build_id = re.sub(r"[\r\n]","",build_id)

user_agent = "Dalvik/2.1.0 (Linux; U; Android {build_version}; {product_model} Build/{build_id})".format(
    build_version = build_version if build_version != "" else "6.0",
    product_model = product_model if product_model != "" else "Nexus 5",
    build_id = build_id if build_id != "" else "MRA58N"
)

def extract(hot_preference):
    domTree = xml.dom.minidom.parseString(hot_preference)
    collection = domTree.documentElement
    for node in collection.getElementsByTagName("string"):
        if node.getAttribute("name") == "ACCOUNT_ID":
            account_id_encrypted = base64.b64decode(node.childNodes[0].nodeValue)
        elif node.getAttribute("name") == "AUTH_TOKEN":
            auth_token_encrypted = base64.b64decode(node.childNodes[0].nodeValue)
    return account_id_encrypted, auth_token_encrypted


def transform(file_01):
    keyOfByte = bytearray(file_01)
    i = 0
    while i < len(keyOfByte):
        temp = keyOfByte[i]
        if i % 2 == 0:
            j = temp & 0xC
            k = temp & 0x3
            temp = temp & 0xF0
            temp = (j >> 2) + temp
            temp = temp + (k << 2)
            keyOfByte[i] = temp
        i = i + 1
    return str(keyOfByte)


def decrypt(key,iv,cipherText):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    unpad = lambda s : s[0:-ord(s[-1])]
    return unpad(cipher.decrypt(cipherText))


iv = file_00
key = transform(file_01)
account_id_encrypted, auth_token_encrypted = extract(hot_preference)

account_id = decrypt(key,iv,account_id_encrypted)
auth_token = decrypt(key,iv,auth_token_encrypted)

print "account-id {}".format(account_id)
print "auth-token {}".format(auth_token)
print "user-agent {}".format(user_agent)

with open(params_path,"w") as file:  
    data = file.write(
        json.dumps({
            "account_id": account_id,
            "auth_token": auth_token,
            "user_agent": user_agent,
            "api_version": "1.3.0"
        },indent = 4)
    )

print "success"
os.system(adb + "kill-server")
sys.stdin.read()