# -*- coding: utf-8 -*-
import sqlite3
import re, json
import os, sys

adb_dir = ".\\platform-tools\\" if os.path.exists("platform-tools") else ""

connect = os.popen(adb_dir + "adb devices").read()
if re.search(r"device\s+$",connect) == None:
    print "can't connect to device"
    os.system(adb_dir + "adb kill-server")
    sys.stdin.read()
    exit()
else:
    print "connect"

commands = [
    'adb shell "su -c cp /data/data/jp.co.sonymusic.communication.keyakizaka/databases/main.db /sdcard/keyakimsg.db"',
    'adb pull /sdcard/keyakimsg.db ./main.db',
    'adb shell "su -c rm /sdcard/keyakimsg.db "',
    'adb kill-server'
]

for command in commands:
    os.popen(adb_dir + command).read()

try:
    connect = sqlite3.connect(".\\main.db")
    cursor = connect.cursor()
except:
    print "open database with something wrong"
    sys.stdin.read()
    exit()

try:
    f = open(".\\download.json","r")
    old = f.read()
    f.close()
    old = json.loads(old)
except:
    old = {}

cursor.execute('''
    SELECT 
    TalkInfo.talkid,
    TalkInfo.mediaType,
    TalentInfo.talentName,
    TalkInfo.sendDateMillis,
    TalkInfo.text
    FROM TalkInfo,TalentInfo 
    WHERE TalkInfo.talentid = TalentInfo.talentid 
    AND mediaType <> 0 
    ORDER BY TalkInfo.sendDateMillis'''
)

db = cursor.fetchall()
connect.close()

new = []
new_add = 0

for i in range(0,len(db)):
    talkId = db[i][0][2:]
    mediaType = db[i][1]

    resource = {
        "talk_id": talkId,
        "media_type": ["photo","audio","video"][mediaType-1],
        "status": 0
    }
    new_add = new_add + 1
    
    if len(old) >= i + 1:
        if old[i]["talk_id"] == talkId:
            resource["status"] = old[i]["status"]
            new_add = new_add - 1

    new.append(resource)

f = open(".\\download.json","w")
f.write(json.dumps(new,indent = 4))
f.close()

print "total {}".format(len(new))
print "new add {}".format(new_add)
print "done"
sys.stdin.read()
exit()

