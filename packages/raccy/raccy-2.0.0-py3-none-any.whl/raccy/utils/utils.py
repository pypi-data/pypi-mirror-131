"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from random import randint
from time import sleep
from urllib.parse import urlparse

import wget
import requests


def download(url, save_path):
    filename = wget.download(url, save_path)
    path = os.path.join(save_path, filename)
    return path


def _get_filepath(filename, save_path):
    return os.path.join(save_path, filename)


def _get_filename(url, save_path):
    fn = os.path.basename(urlparse(url).path)
    fp = _get_filepath(fn, save_path)
    counter = 1
    while True:
        if os.path.isfile(fp):
            fn_split = fn.split('.')
            ext = fn_split.pop()
            fn_without_ext = '.'.join(fn_split)
            temp_fn = f"{fn_without_ext}({counter}).{ext}"
            fp = _get_filepath(temp_fn, save_path)
            counter += 1
            continue
        return fp


def get_filename(url, path, mutex=None):
    if mutex is None:
        return _get_filename(url, path)
    with mutex:
        return _get_filename(url, path)


def download_image(url, save_path, mutex=None):
    response = requests.get(url, allow_redirects=True)
    img_path = get_filename(response.url, save_path, mutex)
    with open(img_path, 'wb') as img:
        img.write(response.content)
    return img_path


def path_exists(path: str, isfile=False) -> bool:
    return os.path.isfile(path) if isfile else os.path.exists(path)


def random_delay(a: int, b: int) -> None:
    sleep(randint(a, b))


def download_delay(a=1, b=5):
    return random_delay(a, b)


def download_delay_per_block(a=1, b=10):
    return random_delay(a, b)


def check_has_attr(obj, attr):
    if not hasattr(obj, attr):
        raise AttributeError(f'{obj} does not have {attr} attribute or method.')
