# -*- coding: utf-8 -*-
import time, re, json
import os, sys, locale, platform
import requests

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass

if platform.system() == "Windows":
    if platform.version() >= "10.0.14393":
        os.system("")
    else:
        import colorama
        colorama.init()

if getattr(sys, "frozen", False):
    work_dir = os.path.dirname(sys.executable)
else:
    work_dir = os.path.dirname(__file__)

# is_python2 = sys.version[0] == "2"
# system_encodeing = sys.stdin.encoding or locale.getpreferredencoding(True)

resource_path = os.path.join(work_dir,"resource")
queue_path = os.path.join(work_dir,"download.json")
params_path = os.path.join(work_dir,"params.json")
pin = ""

def print_fit(string,pin=False):
    if pin == True:
        sys.stdout.write("\r\033[K")
        sys.stdout.write(string)
        sys.stdout.flush()
    else:
        sys.stdout.write(string+"\n")

def quit(string):
    print_fit(string)
    sys.stdin.read()
    exit()

def pin_info(i,amount,media_type):
    global pin
    pin = "{}/{}  {}".format(str(i+1).zfill(len(str(amount))),amount,media_type)

def show_status(status):
    print_fit("{}  {}".format(pin,status),True)

def get_resource_url(talk_id):
    url = "https://client-k.hot.sonydna.com/article"
    data = {
        "article": talk_id,
        "username": username,
        "token": token
    }
    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-Version": api_version
    }

    try:
        show_status("request resource")
        response = requests.request("POST",url,headers=headers,timeout=5,data=json.dumps(data),proxies=proxies)
        json_data = json.loads(response.text)
        resource_url = json_data["result"]["url"]
        show_status("get resource url")
        return resource_url
    except KeyboardInterrupt:
        exit()
    except:
        return None
    

def download_resource(url,file_path):
    if os.path.exists(file_path):
        show_status("file already exists")
        return True
    try:
        show_status("start downloading")
        response = requests.request("GET",url,headers={"User-Agent":user_agent},timeout=5,stream=True,proxies=proxies)
    except KeyboardInterrupt:
        exit()
    except:
        return False

    size = int(response.headers["Content-Length"].strip())
    save = 0

    f = open(file_path,"wb")
    try:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
                save += len(chunk)
                percent = int(float(save)/size*100)
                show_status("downloading...({}%)".format(percent))
    except KeyboardInterrupt:
        exit()
    except:
        f.close()
        os.remove(file_path)
        return False
    else:
        f.close()
        show_status("download successful (100%)")
        return True
        
def file_sync(queue):
    f = open(queue_path,"w")
    f.write(json.dumps(queue,indent = 4,ensure_ascii = False))
    f.close()


def check_format(download_queue):
    talk_id_check = re.compile(r"^\w{64}$")
    for item in download_queue:
        if "status" not in item or "talk_id" not in item: 
            return False
        if not talk_id_check.match(item["talk_id"]): 
            return False
    return True

try:
    f = open(params_path,"r")
    params = f.read()
    params = json.loads(params)
    f.close()
except:
    quit("load params with something wrong")

username = params["account_id"] if "account_id" in params else ""
token = params["auth_token"] if "auth_token" in params else ""
user_agent = params["user_agent"] if "user_agent" in params else ""
api_version = params["api_version"] if "api_version" in params else ""
proxies = {"https": params["proxy"], "http": params["proxy"]} if "proxy" in params else None

if not username or not token or not user_agent or not api_version:
    quit("lack param")

try:
    f = open(queue_path,"r")
    queue = f.read()
    queue = json.loads(queue)
    f.close()
except:
    quit("load queue with something wrong")

if not check_format(queue):
    quit("incorrect queue format")

if not os.path.exists(resource_path): os.mkdir(resource_path)

amount = len(queue)

for index,item in enumerate(queue):
    if item["status"] != 0:
        continue

    media_type = item["media_type"]

    # media_type = ["photo","audio","video"][item["content"]["media_type"] - 1]
    # member_dir = item["content"]["author_name"]
    # member_dir = member_dir.encode(system_encodeing) if is_python2 else member_dir
    # type_dir = ["写真","音声","動画"][item["content"]["media_type"] - 1]
    # type_dir = type_dir.encode(system_encodeing) if is_python2 else type_dir
    # store_dir = os.path.join(resource_path,member_dir,type_dir)
    # if not os.path.exists(store_dir): os.makedirs(store_dir)

    pin_info(index,amount,media_type)
    
    retry = 0
    while True:
        resource_url = get_resource_url(item["talk_id"])
        if resource_url:
            break
        retry += 1
        if retry > 5:
            show_status("request failed")
            break
        show_status("retry {} time(s)".format(retry))
    
    if not resource_url:
        print_fit("")
        continue

    file_name = re.search(r'^\S+/(\S+?)\?\S+$',resource_url).group(1)
    file_path = os.path.join(resource_path,file_name)
    
    # file_extension = os.path.splitext(file_name)[-1]
    # file_name = "{} {} {}{}".format(time.strftime('%Y%m%d %H%M%S',time.localtime(item["content"]["time_stamp"]/1000)),member_dir,type_dir,file_extension)
    # file_path = os.path.join(store_dir,file_name)

    retry = 0
    while True:
        result = download_resource(resource_url,file_path)
        if result:
            queue[index]["status"] = 1
            break
        retry += 1
        if retry > 5:
            show_status("download failed")
            break
        show_status("retry {} time(s)".format(retry))
            
    file_sync(queue)
    print_fit("")
    
quit("all done")