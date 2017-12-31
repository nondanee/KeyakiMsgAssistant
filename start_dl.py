# -*- coding: utf-8 -*-
import re, json, urllib2
import os, sys, locale 

RESOURCE_PATH = ".\\resource"
DOWNLOAD_QUEUE_PATH = ".\\download.json"
PARAMS_PATH = ".\\params.json"
PIN = ""

LANG = 1 if locale.getdefaultlocale()[0] == "zh_CN" else 0
LANG = 0
STRING = {
    "photo":[
        "photo",
        "图片"
    ],
    "video":[
        "video",
        "视频"
    ],
    "audio":[
        "audio",
        "语音"
    ],
    "read_file_error":[
        "read file '%s' with error",
        "打开 %s 文件失败"
    ],
    "lack_param_error":[
        "lack param '%s'",
        "缺少参数 %s "
    ],
    "format_incorrect":[
        "incorrect '%s' format",
        "%s 文件格式不正确"
    ],
    "request_resource":[
        "request resource",
        "请求资源"
    ],
    "request_failed":[
        "request failed",
        "放弃请求"
    ],
    "retry":[
        "retry %d time(s)",
        "重试%d次"
    ],
    "start_download":[
        "start download",
        "开始下载"
    ],
    "download_failed":[
        "download failed",
        "放弃下载"
    ],
    "download_successful":[
        "download successful(%d%%)",
        "下载成功(%d%%)"
    ],
    "downloading":[
        "downloading...(%d%%)",
        "正在下载(%d%%)"
    ],
    "file_exist":[
        "file already exists",
        "文件已存在"
    ],
    "all_done":[
        "all done",
        "已完成"
    ]
}
def get_string(key):
    return STRING[key][LANG]


def printf(string,flush=False):
    if flush == True:
        print "\r" + string.decode("utf-8").encode(sys.stdin.encoding or locale.getpreferredencoding(True)),
        sys.stdout.flush()
    else:
        print string.decode("utf-8").encode(sys.stdin.encoding or locale.getpreferredencoding(True))

def quit(string=None):
    if string != None: printf(string)
    sys.stdin.read()
    exit()

def pin(i,amount,media_type):
    global PIN
    PIN = str(i+1).zfill(len(str(amount))) + "/" + str(amount) + "  " + get_string(media_type) + "  " 

def show_status(process,data=None):
    status = get_string(process)
    if data != None: status = status%(data)
    printf(format("","<40"),True)
    printf(PIN + status,True)

def get_resource_url(talkId):
    url = "https://client-k.hot.sonydna.com/article"
    data = {
        "article":talkId,
        "username":USERNAME,
        "token":TOKEN
    }
    headers = {
        "User-Agent":USER_AGENT,
        "Content-Type":"application/json",
        "Accept":"application/json",
        "X-API-Version":API_VERSION
    }
    request = urllib2.Request(url = url,headers = headers,data = json.dumps(data))
    show_status("request_resource")
    retry = 0
    while True:
        try:
            response = urllib2.urlopen(request,timeout = 3)
            jsondata = json.loads(response.read())
            return jsondata["result"]["url"]
        except Exception as e:
            retry = retry + 1
            if retry >= 10:
                show_status("request_failed")
                return None
            show_status("retry",retry)

def download_resource(url):
    request = urllib2.Request(url = url,headers = {"User-Agent":USER_AGENT})
    show_status("start_download")
    retry = 0
    while True:
        try:
            response = urllib2.urlopen(request,timeout = 5)
            return show_progress(response)
        except Exception as e:
            retry = retry + 1
            if retry >= 10:
                show_status("download_failed")
                return None
            show_status("retry",retry)
                    
def show_progress(response):
    total = response.info().getheader("Content-Length").strip()
    total = int(total)
    byte = 0
    data = ""
    while True:
        chunk = response.read(8192)
        if not chunk:
            break
        byte += len(chunk)
        data += chunk
        percent = float(byte)/total*100
        show_status("downloading",percent)
        
    show_status("download_successful",percent)
    return data

def update_download_queue_file(download_queue):
    f = open(DOWNLOAD_QUEUE_PATH,"w")
    f.write(json.dumps(download_queue,indent = 4))
    f.close()

def check_queue_format(download_queue):
    talk_id_check = re.compile(r"^\w{64}$")
    error_info = get_string("format_incorrect")%"download.json"
    for item in download_queue:
        if "status" not in item or "media_type" not in item or "talk_id" not in item: quit(error_info)
        if item["status"] not in [0,1]: quit(error_info)
        if item["media_type"] not in ["photo","video","audio"]: quit(error_info)
        if talk_id_check.match(item["talk_id"]) == None: quit(error_info)


try:
    f = open(PARAMS_PATH,"r")
    params = f.read()
    params = json.loads(params)
    f.close()
except:
    quit(get_string("read_file_error")%"params.json")

if "account_id" in params: USERNAME = params["account_id"]
else: quit(get_string("lack_param_error")%"account_id")

if "auth_token" in params: TOKEN = params["auth_token"]
else: quit(get_string("lack_param_error")%"auth_token")

if "user_agent" in params: USER_AGENT = params["user_agent"]
else: quit(get_string("lack_param_error")%"user_agent")

if "api_version" in params: API_VERSION = params["api_version"]
else: quit(get_string("lack_param_error")%"api_version")

if "proxy" in params:
    proxy_support = urllib2.ProxyHandler({"https" : params["proxy"], "http" : params["proxy"]})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    
try:
    f = open(DOWNLOAD_QUEUE_PATH,"r")
    download_queue = f.read()
    download_queue = json.loads(download_queue)
    f.close()
except:
    quit(get_string("read_file_error")%"download.json")

check_queue_format(download_queue)

if os.path.exists(RESOURCE_PATH) == False: os.mkdir(RESOURCE_PATH)

amount = len(download_queue)

for i in range(0,amount):
    if download_queue[i]["status"] != 0: continue

    pin(i,amount,download_queue[i]["media_type"])
    resource_url = get_resource_url(download_queue[i]["talk_id"])
    if resource_url != None:
        file_name = re.search(r'^\S+/(\S+?)\?\S+$',resource_url).group(1)
        file_path = RESOURCE_PATH + "\\" + file_name
        if os.path.exists(file_path) == 1:
            show_status("file_exist")
            download_queue[i]["status"] = 1
        else:
            data = download_resource(resource_url)
            if data != None:
                f = open(file_path,'wb')
                f.write(data)
                f.close()
                download_queue[i]["status"] = 1
            
    update_download_queue_file(download_queue)
    printf("")
    
quit(get_string("all_done"))