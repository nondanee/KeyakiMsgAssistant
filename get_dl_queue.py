# -*- coding: utf-8 -*-
import sqlite3
import re, json
import os, sys

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
db_path = os.path.join(work_dir,"main.db")
queue_path = os.path.join(work_dir,"download.json")

connect = os.popen(adb + "devices").read()
if re.search(r"device\s+$",connect):
    print("connect")
else:
    print("can't connect to device")
    os.system(adb + "kill-server")
    sys.stdin.read()
    exit()

commands = [
    "shell su -c cp /data/data/jp.co.sonymusic.communication.keyakizaka/databases/main.db /sdcard/keyakimsg.db",
    "pull /sdcard/keyakimsg.db {}".format(db_path),
    "shell su -c rm /sdcard/keyakimsg.db",
    "kill-server"
]

for command in commands:
    os.popen(adb + command).read()

try:
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
except:
    print("open database with something wrong")
    sys.stdin.read()
    exit()

try:
    f = open(queue_path,"r")
    old = f.read()
    f.close()
    old = json.loads(old)
except:
    old = {}

cursor.execute('''SELECT TalkInfo.talkid, TalkInfo.mediaType, TalentInfo.talentName, TalkInfo.sendDateMillis, TalkInfo.text FROM TalkInfo,TalentInfo  WHERE TalkInfo.talentid = TalentInfo.talentid  AND mediaType <> 0  ORDER BY TalkInfo.sendDateMillis''')
data = cursor.fetchall()
connect.close()

new = []
add = 0

for index,line in enumerate(data):

    if line[1] not in [1,2,3]:
        continue

    talk_id = line[0][2:]

    resource = {
        "talk_id": talk_id,
        "media_type": ["photo","audio","video"][line[1]-1],
        "status": 0
    }

    # resource = {
    #     "talk_id": talk_id,
    #     "content": {
    #         "media_type": line[1],
    #         "author_name": line[2],
    #         "time_stamp": line[3]
    #     },
    #     "status": 0
    # }

    add += 1
    
    if len(old) > index:
        if old[index]["talk_id"] == talk_id:
            resource["status"] = old[index]["status"]
            add -= 1

    new.append(resource)

f = open(queue_path,"w")
f.write(json.dumps(new,indent = 4,ensure_ascii = False))
f.close()

print("total {}".format(len(new)))
print("new add {}".format(add))
print("done")
sys.stdin.read()

