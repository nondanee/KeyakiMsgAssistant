# -*- coding: utf-8 -*-
import os, re, json
import requests
from common import Database, Headers, Proxies, URL

connect = Database()
cursor = connect.cursor()
queue = []

cursor.execute('select groupId, talentName from TalentInfo')
members = cursor.fetchall()
connect.close()

for member in members:
    url = 'https://api.kh.glastonr.net/v2/groups/{}/members'.format(member[0])
    response = requests.request('GET', url, headers = Headers(), proxies = Proxies())
    data = json.loads(response.text)[0]
    if 'thumbnail' in data: queue.append(data['thumbnail'])
    if 'phone_image' in data: queue.append(data['phone_image'])

for url in queue:
    print(url)
    name = os.path.basename(URL(url).path)
    if os.path.exists(name): continue
    response = requests.request('GET', url, headers = Headers(api = False), proxies = Proxies())
    with open(name, 'wb') as f:
        for chunk in response.iter_content(chunk_size = 512):
            if chunk:
                f.write(chunk)