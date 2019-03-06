# -*- coding: utf-8 -*-
import os, sys, platform, time, re, json
import requests

WORKDIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_PATH = os.path.join(WORKDIR, 'download.json')
PARAMS_PATH = os.path.join(WORKDIR, 'params.json')
RESOURCE_PATH = os.path.join(WORKDIR, 'resource')

if platform.system() == 'Windows':
    if platform.version() >= '10.0.14393':
        os.system('')
    else:
        import colorama
        colorama.init()

pinned = ''

def log(string, wrap = True):
    if wrap == False:
        sys.stdout.write('\r\033[K')
        sys.stdout.write(string)
        sys.stdout.flush()
    else:
        sys.stdout.write(string + '\n')

def quit(string):
    log(string)
    sys.stdin.read()
    exit()    

def show_status(status):
    log('{}  {}'.format(pinned, status), False)

def query_resource(talk_id):
    url = 'https://client-k.hot.sonydna.com/article'
    data = {
        'article': talk_id,
        'username': params['account_id'],
        'token': params['auth_token']
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': params['user_agent'],
        'X-API-Version': params['api_version']
    }

    try:
        show_status('request resource')
        response = requests.request(
            'POST', url, headers = headers, data = json.dumps(data),
            timeout = 5, proxies = proxies
        )
        json_data = json.loads(response.text)
        resource_url = json_data['result']['url']
        show_status('get resource url')
        return resource_url
    except KeyboardInterrupt:
        exit()
    except:
        return None
    
def download_file(url, path):
    if os.path.exists(path):
        show_status('file already exists')
        return True
    try:
        show_status('start downloading')
        response = requests.request(
            'GET', url, headers = {'User-Agent': params['user_agent']}, 
            timeout = 5, stream = True, proxies = proxies
        )
    except KeyboardInterrupt:
        exit()
    except:
        return False

    size = int(response.headers['Content-Length'].strip())
    save = 0

    file = open(path, 'wb')
    try:
        for chunk in response.iter_content(chunk_size = 512):
            if chunk:
                file.write(chunk)
                save += len(chunk)
                percent = int(float(save) / size * 100)
                show_status('downloading...({}%)'.format(percent))
    except KeyboardInterrupt:
        file.close()
        if os.path.exists(path): os.remove(path)
        exit()
    except:
        file.close()
        if os.path.exists(path): os.remove(path)
        return False
    else:
        file.close()
        return True

def file_sync(path, data):
    file = open(path, 'w')
    file.write(json.dumps(data, indent = 4, ensure_ascii = False))
    file.close()

def format_check(queue):
    talk_id_check = re.compile(r'^\w{64}$')
    for item in queue:
        if 'status' not in item or 'talk_id' not in item:
            return False
        if not talk_id_check.match(item['talk_id']):
            return False
    return True

try:
    with open(PARAMS_PATH, 'r') as params_file:
        params = json.loads(params_file.read())
except:
    quit('load params with something wrong')

for key in ['account_id', 'auth_token', 'user_agent', 'api_version']:
    if key not in params:
        quit('lack param')

proxies = {'https': "params['proxy']", 'http': params['proxy']} if 'proxy' in params else None

try:
    with open(QUEUE_PATH, 'r') as queue_file:
        queue = json.loads(queue_file.read())
except:
    quit('load queue with something wrong')

if not format_check(queue):
    quit('incorrect queue format')

if not os.path.exists(RESOURCE_PATH):
    os.mkdir(RESOURCE_PATH)

amount = len(queue)

for index, item in enumerate(queue):
    if item['status'] != 0: continue

    media_type = item['media_type']

    # media_type = ['photo','audio','video'][item['content']['media_type'] - 1]
    # member_dir = item['content']['author_name']
    # member_dir = member_dir.encode(system_encodeing) if is_python2 else member_dir
    # type_dir = ['写真','音声','動画'][item['content']['media_type'] - 1]
    # type_dir = type_dir.encode(system_encodeing) if is_python2 else type_dir
    # store_dir = os.path.join(resource_path,member_dir,type_dir)
    # if not os.path.exists(store_dir): os.makedirs(store_dir)

    pinned = '{}/{}  {}'.format(str(index + 1).zfill(len(str(amount))), amount, media_type)

    for retry in range(6):
        if retry != 0: show_status('retry {} time(s)'.format(retry))
        url = query_resource(item['talk_id'])
        if url: break

    if not url:
        show_status('query failed')
        log('')
        continue

    name = re.search(r'^\S+/(\S+?)\?\S+$', url).group(1)
    path = os.path.join(RESOURCE_PATH, name)

    # file_extension = os.path.splitext(file_name)[-1]
    # file_name = '{} {} {}{}'.format(time.strftime('%Y%m%d %H%M%S',time.localtime(item['content']['time_stamp']/1000)),member_dir,type_dir,file_extension)
    # file_path = os.path.join(store_dir,file_name)

    for retry in range(6):
        if retry != 0: show_status('retry {} time(s)'.format(retry))
        success = download_file(url, path)
        if success: break

    if not success:
        show_status('download failed')
    else:
        show_status('download successful')
        queue[index]['status'] = 1

    log('')
    file_sync(QUEUE_PATH, queue)

quit('all done')