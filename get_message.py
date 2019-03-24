# -*- coding: utf-8 -*-
import os, sys, re, time, sqlite3
import adb

WORKDIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(WORKDIR, 'main.db')
RESOURCE_PATH = os.path.join(WORKDIR, 'resource')
FILE_NAME = 'テキスト.txt'

if adb.connect():
    print('connect')
else:
    print("can't connect to device")
    os.system('pause')
    exit()

commands = [
    '''shell "su -c 'cp /data/data/jp.co.sonymusic.communication.keyakizaka/databases/main.db /sdcard/keyakimsg.db'"''',
    'pull /sdcard/keyakimsg.db ' + DATABASE_PATH,
    '''shell "su -c 'rm /sdcard/keyakimsg.db'"''',
    'kill-server'
]

with open(DATABASE_PATH, 'w') as database_file:
    database_file.close()

for command in commands:
    adb.execute(command)

try:
    connect = sqlite3.connect(DATABASE_PATH)
    cursor = connect.cursor()
except:
    print('open database with something wrong')
    os.system('pause')
    exit()

cursor.execute('select nickname from ProfileInfo limit 1')
nickname = cursor.fetchone()[0]
cursor.execute('select talentName from TalentInfo')
members = cursor.fetchall()
cursor.execute('select TalkInfo.talkid,TalkInfo.mediaType,TalentInfo.talentName,TalkInfo.sendDateMillis,TalkInfo.text from TalkInfo,TalentInfo where TalkInfo.talentid = TalentInfo.talentid order by TalentInfo.talentName,TalkInfo.sendDateMillis desc')
data = cursor.fetchall()
connect.close()

message = {member[0]: '' for member in members}

for line in data:
    talk_id, media_type, talent_name, send_date_millis, text = line
    sent_time = time.strftime('%Y-%m-%d %X', time.localtime(send_date_millis/1000))
    text = text.replace('%%%', nickname)

    if media_type not in [0, 1, 2, 3]:
        continue

    if media_type != 0:
        text = ['[写真]', '[音声]', '[動画]'][media_type - 1] + text
    
    message[talent_name] += '{} {}\n{}\n\n'.format(sent_time, talent_name, text)

if not os.path.exists(RESOURCE_PATH): os.mkdir(RESOURCE_PATH)

for name in message: 
    archive = os.path.join(RESOURCE_PATH, name)
    if not os.path.exists(archive): os.mkdir(archive)
    with open(os.path.join(archive, FILE_NAME), 'w', encoding = 'utf-8') as f:
        f.write(message[name])

print('total {}'.format(len(data)))
os.system('pause')