# -*- coding: utf-8 -*-
import os, sys, re, json, sqlite3
import adb

if adb.connect():
    print('connect')
else:
    print("can't connect to device")
    os.system('pause')
    exit()

commands = [
    '''shell "su -c 'cp /data/data/jp.co.sonymusic.communication.keyakizaka/databases/main.db /sdcard/keyakimsg.db'"''',
    'pull /sdcard/keyakimsg.db ./main.db',
    '''shell "su -c 'rm /sdcard/keyakimsg.db'"''',
    'kill-server'
]

for command in commands:
    adb.execute(command)

try:
    connect = sqlite3.connect('./main.db')
    cursor = connect.cursor()
except:
    print('open database with something wrong')
    os.system('pause')
    exit()

try:
    with open('./download.json', 'r') as queue_file:
        old = json.loads(queue_file.read())
except:
    old = []

cursor.execute('''
    SELECT TalkInfo.talkid, TalkInfo.mediaType, TalentInfo.talentName, TalkInfo.sendDateMillis, TalkInfo.text
    FROM TalkInfo, TalentInfo
    WHERE TalkInfo.talentid = TalentInfo.talentid AND mediaType <> 0
    ORDER BY TalkInfo.sendDateMillis
''')
data = cursor.fetchall()
connect.close()

new = []
add = 0

for index, line in enumerate(data):

    if line[1] not in [1, 2, 3]:
        continue

    talk_id = line[0][2:]

    resource = {
        'talk_id': talk_id,
        'media_type': ['photo', 'audio', 'video'][line[1]-1],
        'status': 0
    }

    # resource = {
    #     'talk_id': talk_id,
    #     'content': {
    #         'media_type': line[1],
    #         'author_name': line[2],
    #         'time_stamp': line[3]
    #     },
    #     'status': 0
    # }

    add += 1
    
    if len(old) > index:
        if old[index]['talk_id'] == talk_id:
            resource['status'] = old[index]['status']
            add -= 1

    new.append(resource)

with open('./download.json', 'w') as queue_file:
    queue_file.write(json.dumps(new, indent = 4, ensure_ascii = False))

print('total {}\nnew add {}\ndone'.format(len(new), add))
os.system('pause')

