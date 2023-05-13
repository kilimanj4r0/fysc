from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import asyncio
import aiohttp

import requests
import hashlib
import json
import os
from typing import List, Dict

import time
import traceback


DATA_DIR_BASE = 'data'
YANDEX_URL_BASE = 'https://cloud-api.yandex.net/v1/disk/public/resources'


router = APIRouter(
    prefix="/detector"
)


def create_empty_file(filename, size_in_bytes):
    if os.path.isfile(filename):
        return

    with open(filename, 'wb') as f:
        f.seek(size_in_bytes-1)
        f.write(b'\0')


async def download_file(url: str, path: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(path, 'wb') as f:
                f.write(data)


async def download_files(path: str, files: List[Dict[str, str]]) -> None:
    tasks = [asyncio.create_task(download_file(file['url'], os.path.join(path, file['filename']))) for file in files]
    await asyncio.gather(*tasks)


@router.get("/find")
async def find(target_album_url: str=None, reference_album_url: str=None):
    if target_album_url is None:
        raise HTTPException(status_code=400,
            detail='Missing target_album_url query parameter')
    if reference_album_url is None:
        raise HTTPException(status_code=400,
            detail='Missing reference_album_url query parameter')

    target_url_hash = hashlib.md5()
    target_url_hash.update(target_album_url.encode())
    reference_url_hash = hashlib.md5()
    reference_url_hash.update(reference_album_url.encode())

    target_dir = os.path.join(DATA_DIR_BASE, target_url_hash.hexdigest())
    reference_dir = os.path.join(DATA_DIR_BASE, reference_url_hash.hexdigest())

    if not os.path.isdir(target_dir):
        os.makdirs(target_dir)
        target_download_links = get_photos_from_yandex(target_album_url)
        await download_files(target_dir, target_download_links)
    if not os.path.isdir(reference_dir):
        os.makedirs(reference_dir)
        reference_download_links = get_photos_from_yandex(reference_album_url)
        await download_files(reference_dir, reference_album_url)
    


    return 'success'


def get_photos_from_yandex(public_key: str):
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
            photo_download_links.append({'url': item['file'], 'filename': item['name']})

    return photo_download_links


# _response = requests.get('https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key=https://disk.yandex.ru/d/ou7SOIOnzNwU-w&fields=_embedded.items')
# _response = requests.get('https://cloud-api.yandex.net/v1/disk/public/resources?public_key=https://disk.yandex.ru/d/ou7SOIOnzNwU-w/IMG20230303180318.jpg', headers={'Authorization': 'OAuth y0_AgAAAABUgujhAADLWwAAAADgEmGGshmNSLZhQmmWQrtNF1whqHr1Fgw'})
