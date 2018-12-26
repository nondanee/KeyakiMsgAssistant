# -*- coding: utf-8 -*-
import os, re, json, sqlite3, requests

WORKDIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_PATH = os.path.join(WORKDIR, 'params.json')
DATABASE_PATH = os.path.join(WORKDIR, 'main.db')

with open(PARAMS_PATH, 'r') as f:
    params = json.loads(f.read())

connect = sqlite3.connect(DATABASE_PATH)
cursor = connect.cursor()
queue = []

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': params['user_agent'],
    'X-API-Version': params['api_version']
}

cursor.execute('select talentId, talentName from TalentInfo')
members = cursor.fetchall()
cursor.execute('select min(talkId) from TalkInfo where mediaType = 2 group by talentId')
telephones = cursor.fetchall()
connect.close()

for member in members:
    response = requests.request(
        'POST', 'https://client-k.hot.sonydna.com/author/info',
        headers = headers,
        data = json.dumps({'author': member[0], 'username': params['account_id'], 'token': params['auth_token']})
    )

    body = json.loads(response.text)
    queue.append(body['result']['thumbnail'])

for telephone in telephones:
    response = requests.request(
        'POST', 'https://client-k.hot.sonydna.com/article',
        headers = headers,
        data = json.dumps({'article': telephone[0][2:], 'username': params['account_id'], 'token': params['auth_token']})
    )
    body = json.loads(response.text)
    queue.append(body['result']['phoneimage'])

for url in queue:
    print(url)
    response = requests.request('GET', url, headers = headers)
    with open(re.search(r'^\S+/(\S+?)\?\S+$', url).group(1), 'wb') as f:
        for chunk in response.iter_content(chunk_size = 512):
            if chunk:
                f.write(chunk)