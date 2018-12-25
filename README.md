<img src="https://raw.githubusercontent.com/nondanee/KeyakiMsgAssistant-Xposed/master/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png" alt="logo" width="144" height="144" align="right" />

# KeyakiMsgAssistant ![](https://img.shields.io/badge/python-3.4%2B-blue.svg)
CLI tool for extracting resources from "欅坂46メッセー" app

## Requirement
- [x] Rooted
- [x] ADB tool
- [x] Python environment

## Implementation
- Pull profile files from device
- Decrypt data to get access token
- Forge requests for resource urls 
- Download media files to local 

## Usage
#### 1. Get parameters (ADB Required)
Run ```python get_params.py``` in terminal

![](https://user-images.githubusercontent.com/26399680/50423451-70a9cd80-0890-11e9-9f7a-27890cc82a41.jpg)

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

![](https://user-images.githubusercontent.com/26399680/50423452-71dafa80-0890-11e9-8b12-3f7a4e6f8bd9.jpg)

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

![](https://user-images.githubusercontent.com/26399680/50423450-6f78a080-0890-11e9-80f7-a633b5051826.jpg)

All media files are downloaded to ```./resource``` directory

![](https://user-images.githubusercontent.com/26399680/50423454-730c2780-0890-11e9-8f46-10c7ef8eeb40.jpg)

Enjoy yourself


## License
This project is under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)