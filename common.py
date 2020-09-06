import os, json, sqlite3, urllib, time
import requests
import adb

WORKDIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_PATH = os.path.join(WORKDIR, 'params.json')
DATABASE_PATH = os.path.join(WORKDIR, 'main.db')
QUEUE_PATH = os.path.join(WORKDIR, 'download.json')
RESOURCE_PATH = os.path.join(WORKDIR, 'resource')
NOW = lambda : int(round(time.time() * 1000))

params = None
def load_params():
    global params
    try:
        with open(PARAMS_PATH, 'r') as params_file:
            params = json.loads(params_file.read())
    except:
        print('load params with something wrong')
        exit()

def update_params():
    global params
    url = 'https://api.kh.glastonr.net/v2/update_token'
    data = json.dumps({ 'refresh_token' : params['authorization']['refresh_token'] })
    response = requests.request('POST', url, headers = Headers(token = False), data = data, proxies = Proxies())
    body = json.loads(response.text)
    now = NOW()
    params['authorization'] = {
        'access_token': body['access_token'],
        'refresh_token': body['refresh_token'],
        'access_token_lives_at': now,
        'access_token_expires_at': now + (body['expires_in'] * 1000)
    }
    with open(PARAMS_PATH, 'w') as f:
        f.write(json.dumps(params, indent = 4))

def ADB():
    if adb.connect():
        print('connect')
        return adb
    else:
        print("can't connect to device")
        os.system('pause')
        exit()

def URL(url):
    return urllib.parse.urlsplit(url)

def Proxies():
    if not params: load_params()
    if 'proxy' in params:
        return { 'https': params['proxy'], 'http': params['proxy'] }
    else:
        return None

def Headers(*, api = True, token = True):
    if not params: load_params()
    headers = {}
    headers['User-Agent'] = params['user_agent']
    if not api: return headers
    headers['Accept'] = 'application/json'
    headers['Content-Type'] = 'application/json'
    headers['X-Talk-App-ID'] = params['app_id']
    authorization = params['authorization']
    if not token: return headers
    if NOW() + 60 * 1e3 > authorization['access_token_expires_at']: update_params()
    headers['Authorization'] = 'Bearer {}'.format(params['authorization']['access_token'])
    return headers

def Database():
    ADB()
    commands = [
        '''shell "su -c 'cp /data/data/jp.co.sonymusic.communication.keyakizaka/databases/main.db /sdcard/keyakimsg.db'"''',
        'pull /sdcard/keyakimsg.db ' + DATABASE_PATH,
        '''shell "su -c 'rm /sdcard/keyakimsg.db'"''',
        'kill-server'
    ]
    for command in commands: adb.execute(command)
    adb.kill()

    try:
        return sqlite3.connect(DATABASE_PATH)
    except:
        print('open database with something wrong')
        os.system('pause')
        exit()
