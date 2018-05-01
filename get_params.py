# -*- coding: utf-8 -*-
import os, sys, platform, subprocess
import xml.dom.minidom, base64
import re, json
from Crypto.Cipher import AES

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass

if getattr(sys, "frozen", False):
    work_dir = os.path.dirname(sys.executable)
else:
    work_dir = os.path.dirname(__file__)

adb_dir = os.path.join(work_dir,"platform-tools") 
adb_dir = adb_dir if os.path.exists(adb_dir) else ""
adb = os.path.join(adb_dir,"adb") + " "
params_path = os.path.join(work_dir,"params.json")

connect = os.popen(adb + "devices").read()
if re.search(r"device\s+$",connect):
    print("connect")
else:
    print("can't connect to device")
    os.system(adb + "kill-server")
    sys.stdin.read()
    exit()

command_00 = "adb shell su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_00"
command_01 = "adb shell su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_01"
command_00 = command_00 if platform.system() == "Windows" or not adb_dir else "./" + command_00
command_01 = command_01 if platform.system() == "Windows" or not adb_dir else "./" + command_01
pipe_00 = subprocess.Popen(command_00,shell=True,stdout=subprocess.PIPE,cwd=adb_dir if adb_dir else None)
pipe_01 = subprocess.Popen(command_01,shell=True,stdout=subprocess.PIPE,cwd=adb_dir if adb_dir else None)
file_00 = pipe_00.stdout.read()
file_01 = pipe_01.stdout.read()
# file_00 = os.popen(adb + "shell su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_00",'rb').read()
# file_01 = os.popen(adb + "shell su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/files/file_01",'rb').read()
hot_preference = os.popen(adb + "shell su -c cat /data/data/jp.co.sonymusic.communication.keyakizaka/shared_prefs/hot_preference.xml").read()

product_model = os.popen(adb + "shell getprop ro.product.model").read().strip()
build_version = os.popen(adb + "shell getprop ro.build.version.release").read().strip()
build_id = os.popen(adb + "shell getprop ro.build.id").read().strip()

user_agent = "Dalvik/2.1.0 (Linux; U; Android {build_version}; {product_model} Build/{build_id})".format(
    build_version = build_version if build_version else "6.0",
    product_model = product_model if product_model else "Nexus 5",
    build_id = build_id if build_id else "MRA58N"
)


def extract(string):
    dom_tree = xml.dom.minidom.parseString(string)
    collection = dom_tree.documentElement
    for node in collection.getElementsByTagName("string"):
        if node.getAttribute("name") == "ACCOUNT_ID":
            account_id_encrypted = base64.b64decode(node.childNodes[0].nodeValue)
        elif node.getAttribute("name") == "AUTH_TOKEN":
            auth_token_encrypted = base64.b64decode(node.childNodes[0].nodeValue)
    return account_id_encrypted, auth_token_encrypted


def transform(string):
    byte_array = bytearray(string)
    i = 0
    while i < len(byte_array):
        temp = byte_array[i]
        if i % 2 == 0:
            j = temp & 0xC
            k = temp & 0x3
            temp = temp & 0xF0
            temp = (j >> 2) + temp
            temp = temp + (k << 2)
            byte_array[i] = temp
        i = i + 1
    return bytes(byte_array)


def decrypt(key,iv,cipher_text):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.decrypt(cipher_text).rstrip().decode()


try:
    iv = file_00
    key = transform(file_01)
    account_id_encrypted, auth_token_encrypted = extract(hot_preference)
    account_id = decrypt(key,iv,account_id_encrypted)
    auth_token = decrypt(key,iv,auth_token_encrypted)
except Exception as e:
    print("error")
    sys.stdin.read()
    exit()

print("account-id {}".format(account_id))
print("auth-token {}".format(auth_token))
print("user-agent {}".format(user_agent))

with open(params_path,"w") as params_file:
    data = params_file.write(
        json.dumps({
            "account_id": account_id,
            "auth_token": auth_token,
            "user_agent": user_agent,
            "api_version": "1.3.0"
        },indent = 4)
    )

print("success")
os.system(adb + "kill-server")
sys.stdin.read()