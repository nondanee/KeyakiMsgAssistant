<img src="https://user-images.githubusercontent.com/26399680/54876133-64a8ba00-4e45-11e9-811e-85ddc22b66be.png" alt="logo" width="144" height="144" align="right" />

# KeyakiMsgAssistant ![](https://img.shields.io/badge/python-3.4+-blue.svg?style=flat-square)

CLI tool for extracting resources from "欅坂46メッセー" app

## Requirement

- [x] Rooted
- [x] ADB tool
- [x] Python environment

## Implementation

- Extract profile and database from device
- Decrypt access token and get resource id
- Forge requests for resource urls
- Download media files to local

## Dependency

```
pip install pycryptodome requests
```

## Usage

#### 1. Get parameters (ADB Required)

Run `python get_params.py` in terminal

![](https://user-images.githubusercontent.com/26399680/54876702-3d56ea80-4e4f-11e9-908c-9634500882b6.png)

Program will generate `params.json` like

```
{
    "auth_token": "????????-????-????-????-????????????", 
    "account_id": "????????-????-????-????-????????????", 
    "api_version": "?.?.?", 
    "user_agent": "Dalvik/2.1.0 (Linux; U; Android ?????; ????? Build/??????)",
}
```

If you want to use proxy, add a line like

```
    "proxy": "http://127.0.0.1:1080",
```

This step is only needed when run for the first time or after changing login device

#### 2. Get download queue (ADB Required)

Run `python get_dl_queue.py` in terminal

![](https://user-images.githubusercontent.com/26399680/54876703-3d56ea80-4e4f-11e9-8b60-b43361f4f6cb.png)

Program will pull SQLite file `main.db` from device to working directory

and generate `download.json` like

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

`"status": 1` means media file has already downloaded

#### 3. Start download

Run `python start_dl.py` in terminal

![](https://user-images.githubusercontent.com/26399680/54876704-3d56ea80-4e4f-11e9-88f7-5643bd37eb61.png)

All media files are downloaded to `./resource` directory

![](https://user-images.githubusercontent.com/26399680/54876851-d424a680-4e51-11e9-8a36-ab3f935dd172.png)

Enjoy yourself

## License
This project is under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)