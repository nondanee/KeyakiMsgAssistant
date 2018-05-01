<img src="https://raw.githubusercontent.com/nondanee/KeyakiMsgAssistant-Xposed/master/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png" alt="logo" width="144" height="144" align="right" />

# KeyakiMsgAssistant
CLI tool for extracting resources from "欅坂46メッセー" app  
Compatible with both Python 2 and Python 3  
Packaged executable files with Out-of-Box experience can be found in release tag

## Requirement
- [x] Rooted
- [ ] ADB tool
- [ ] Python environment

## Description
- Pull needed files from device
- Decrypt data to get access token
- Forge requests for resource urls 
- Download media files to local 

## Usage
#### 1. Get parameters (ADB Required)
Run ```python get_params.py``` in terminal

<img src="/screenshots/params.jpg" alt="get_params" align="center" />

Generate ```params.json``` like
```
{
    "auth_token": "????????-????-????-????-????????????", 
    "account_id": "????????-????-????-????-????????????", 
    "api_version": "1.3.0", 
    "user_agent": "Dalvik/2.1.0 (Linux; U; Android ?????; ????? Build/??????)",
}
```
If you want to use proxy, add a line like
```
    "proxy": "http://127.0.0.1:1080",
```

#### 2. Get download queue (ADB Required)
Run ```python get_dl_queue.py``` in terminal

<img src="/screenshots/queue.jpg" alt="get_dl_queue" align="center" />

Pull sqlite3 file ```main.db``` from device to working directory  
Generate ```download.json``` like
```
[
    ......
    {
        "status": 0, 
        "media_type": "photo", 
        "talk_id": "6444219f8da00a2af0f81ad747de8bba6d0dd2cb556fee9c22d21828316a6ee7"
    },
    ......
]
```
as download queue which supports progress reserved and incremental update

```"status": 1``` means media file has already downloaded

#### 3. Start download
Run ```python start_dl.py``` in terminal

<img src="/screenshots/dl.jpg" alt="start_dl" align="center" />

All media files are downloaded to ```./resource``` directory

<img src="/screenshots/resource.jpg" alt="resource" align="center" />

Enjoy yourself


## License
This project is under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)