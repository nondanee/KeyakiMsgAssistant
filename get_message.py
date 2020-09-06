# -*- coding: utf-8 -*-
import os, time
from common import Database, RESOURCE_PATH

FILE_NAME = 'テキスト.txt'

connect = Database()
cursor = connect.cursor()

cursor.execute('select nickname from ProfileInfo limit 1')
nickname = cursor.fetchone()[0]
cursor.execute('select talentName from TalentInfo')
members = cursor.fetchall()
cursor.execute('select TalkInfo.talkid, TalkInfo.mediaType, TalentInfo.talentName, TalkInfo.sendDateMillis, TalkInfo.text from TalkInfo, TalentInfo where TalkInfo.talentid = TalentInfo.talentid order by TalentInfo.talentName, TalkInfo.sendDateMillis desc')
data = cursor.fetchall()
connect.close()

message = { member[0]: '' for member in members }

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