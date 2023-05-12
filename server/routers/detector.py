from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import requests
import hashlib
import json
import os

import time


router = APIRouter(
    prefix="/detector"
)


def create_empty_file(filename, size_in_bytes):
    if os.path.isfile(filename):
        return

    with open(filename, 'wb') as f:
        f.seek(size_in_bytes-1)
        f.write(b'\0')


@router.get("/find")
async def find(target_album_url: str=None, reference_album_url: str=None):
    time.sleep(15)
    create_empty_file(os.path.join(DATA_DIR_BASE, 'dummy.zip'), 256 * 1024 * 1024)

    def file_iterator(file_path, chunk_size=4096):
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(
        file_iterator(os.path.join(DATA_DIR_BASE, 'dummy.zip')),
        media_type='application/zip',
    )

    # if target_album_url is None:
    #     return 'target is none'
    # # if reference_album_url is None:
    # #     return 'reference is none'

    # target_url_hash = hashlib.md5().update(target_album_url)
    # # reference_url_hash = hashlib.md5().update(reference_album_url)

    # target_dir = os.path.join(DATA_DIR_BASE, target_url_hash.hexdigest())
    # reference_dir = os.path.join(DATA_DIR_BASE, reference_url_hash.hexdigest())

    # if os.path.isdir(target_dir)
    
    # try:
    #     target_download_links = get_from_yandex(target_album_url)
    # except Exception:
    #     return traceback.format_exc()

    # return target_download_links


DATA_DIR_BASE = ''
YANDEX_URL_BASE = 'https://cloud-api.yandex.net/v1/disk/public/resources'


def get_from_yandex(public_key: str):
    url = YANDEX_URL_BASE + f'?public_key={public_key}'
    response = requests.get(url)

    if response.status_code != 200:
        return

    photo_download_links = []
    items = json.loads(response.content)['_embedded']['items']
    for item in items:
        if item['type'] == 'dir':
            pass
        elif item['type'] == 'file' and item['media_type'] == 'image':
            photo_download_links.append(item['file'])

    return photo_download_links


# _response = requests.get('https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key=https://disk.yandex.ru/d/ou7SOIOnzNwU-w&fields=_embedded.items')
# _response = requests.get('https://cloud-api.yandex.net/v1/disk/public/resources?public_key=https://disk.yandex.ru/d/ou7SOIOnzNwU-w/IMG20230303180318.jpg', headers={'Authorization': 'OAuth y0_AgAAAABUgujhAADLWwAAAADgEmGGshmNSLZhQmmWQrtNF1whqHr1Fgw'})
