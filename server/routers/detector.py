import io
import os
import json
import asyncio
import hashlib
import zipfile
from typing import List, Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

import aiohttp
import requests

from deepface import DeepFace


DATA_DIR_BASE = 'data'
YANDEX_URL_BASE = 'https://cloud-api.yandex.net/v1/disk/public/resources'

DISTANCE_METRIC = 'euclidean_l2'
MODEL_NAME = 'Facenet512'
DETECTOR_BACKEND = 'retinaface'


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
async def find(input_album_url: str=None, reference_album_url: str=None):
    if input_album_url is None:
        raise HTTPException(status_code=400,
            detail='Missing input_album_url query parameter')
    if reference_album_url is None:
        raise HTTPException(status_code=400,
            detail='Missing reference_album_url query parameter')

    input_url_hash = hashlib.md5()
    input_url_hash.update(input_album_url.encode())
    reference_url_hash = hashlib.md5()
    reference_url_hash.update(reference_album_url.encode())

    input_dir = os.path.join(DATA_DIR_BASE, input_url_hash.hexdigest())
    reference_dir = os.path.join(DATA_DIR_BASE, reference_url_hash.hexdigest())

    if not os.path.isdir(input_dir):
        os.makedirs(input_dir)
        input_download_links = get_photos_from_yandex(input_album_url)
        await download_files(input_dir, input_download_links)
    if not os.path.isdir(reference_dir):
        os.makedirs(reference_dir)
        reference_download_links = get_photos_from_yandex(reference_album_url)
        await download_files(reference_dir, reference_download_links)

    for dirpath, _, filenames in os.walk(reference_dir):
        output_file_paths = []
        for filename in filenames:
            reference_path = os.path.join(dirpath, filename)

            df = DeepFace.find(
                img_path=reference_path,
                db_path=input_dir,
                enforce_detection=False,
                distance_metric=DISTANCE_METRIC,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
            )
            output_file_paths += list(df[0]['identity'])

    output_file_paths = set(output_file_paths)
    outupt_archive_filename = input_url_hash.hexdigest() + '.zip'

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zipf:
        for output_file_path in output_file_paths:
            zipf.write(output_file_path,
                       arcname=os.path.basename(output_file_path))
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type='application/zip',
        headers={
            'Access-Control-Expose-Headers': 'Content-Disposition', 
            'Content-Disposition':
                f'attachment; filename={outupt_archive_filename}',
        }
    )


def get_photos_from_yandex(public_key: str):
    url = YANDEX_URL_BASE + f'?public_key={public_key}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception

    photo_download_links = []
    items = json.loads(response.content)['_embedded']['items']
    for item in items:
        if item['type'] == 'dir':
            pass
        elif item['type'] == 'file' and item['media_type'] == 'image':
            photo_download_links.append({
                'url': item['file'],
                'filename': item['name'],
            })

    return photo_download_links
