<img src="https://user-images.githubusercontent.com/26399680/54876133-64a8ba00-4e45-11e9-811e-85ddc22b66be.png" alt="logo" width="144" height="144" align="right" />

# KeyakiMsgAssistant ![](https://img.shields.io/badge/python-3.4+-blue.svg?style=flat-square)

CLI tool for extracting resources from "欅坂46/日向坂46 メッセージ" app

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

![](https://user-images.githubusercontent.com/26399680/92327663-d69eae80-f08d-11ea-866d-da3da48e1aec.png)

Program will generate `params.json` like

```json
{
    "authorization": {
        ...
    },
    "user_agent": ...,
    "app_id": ...
}
```

If you want to use proxy, add a line like

```json
    "proxy": "http://127.0.0.1:1080",
```

This step is only needed when run for the first time or after changing login device

#### 2. Get download queue (ADB Required)

Run `python get_dl_queue.py` in terminal

![](https://user-images.githubusercontent.com/26399680/54876703-3d56ea80-4e4f-11e9-8b60-b43361f4f6cb.png)

Program will pull SQLite file `main.db` from device to working directory

and generate `download.json` like

```json
[
    ...,
    {
        "status": 0,
        "media_type": "photo",
        "talk_id": "0000007527"
    },
    ...
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