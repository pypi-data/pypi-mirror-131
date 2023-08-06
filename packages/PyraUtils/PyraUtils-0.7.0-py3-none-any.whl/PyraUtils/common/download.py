#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created by：2018-2-23 14:15:57
modify by: 2021-12-03 15:05:05

功能：各种常用的方法函数的封装。
"""

import urllib
import shutil
from contextlib import closing
import requests
import httpx
import rich.progress
from tqdm import tqdm

class DownloadUtil:
    """DownloadUtil, 工具类

    Attributes:

    """

    @staticmethod
    def dl_01(url, dl_path, **kwargs):
        # open in binary mode
        with open(dl_path, "wb") as out_file:
            try:
                resp = requests.get(url, kwargs)
                out_file.write(resp.content)
            except (requests.HTTPError, requests.Timeout,
                    requests.exceptions.URLRequired) as err:
                print(err)

    @staticmethod
    def dl_02(url, dl_path, **kwargs):
        req = urllib.request.Request(url, kwargs)
        with urllib.request.urlopen(req) as resp, open(dl_path, 'wb') as out_file:
            shutil.copyfileobj(resp, out_file)

    @staticmethod
    def dl_03(url, dl_path, **kwargs):
        with closing(requests.get(url, kwargs)) as resp:
            resp_code = resp.status_code
            if 299 < resp_code or resp_code < 200:
                print('returnCode %s %s' % (resp_code, url))

            content_length = int(resp.headers.get('content-length', '0'))
            if content_length == 0:
                print('size0 %s' % url)

            try:
                with open(dl_path, 'wb') as f:
                    for data in resp.iter_content(1024):
                        f.write(data)
            except Exception as err:
                print('Savefail %s, %s' % (url, err))

    @staticmethod
    def dl_large(url, dl_path, chunk_size=512 * 1024, **kwargs):
        with open(dl_path, "wb") as out_file:
            try:
                resp = requests.get(url, kwargs)
                for chunk in resp.iter_content(chunk_size=chunk_size): 
                    out_file.write(chunk)
            except (requests.HTTPError, requests.Timeout,
                    requests.exceptions.URLRequired) as err:
                print(err)

class DownloadProgressUtil:
    """DownloadProgressUtil, 工具类

    Attributes:

    """
    @staticmethod
    def dl_progress(url, dl_path, **kwargs):
        with open(dl_path, 'wb', kwargs) as out_file:
            with httpx.stream("GET", url) as resp:
                total = int(resp.headers["Content-Length"])

                with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                    num_bytes_downloaded = resp.num_bytes_downloaded
                    for chunk in resp.iter_bytes():
                        out_file.write(chunk)
                        progress.update(resp.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = resp.num_bytes_downloaded


    @staticmethod
    def dl_rich_progress(url, dl_path, **kwargs):
        with open(dl_path, 'wb') as out_file:
            with httpx.stream("GET", url, kwargs) as resp:
                total = int(resp.headers["Content-Length"])

                with rich.progress.Progress(
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    rich.progress.BarColumn(bar_width=None),
                    rich.progress.DownloadColumn(),
                    rich.progress.TransferSpeedColumn(),
                ) as progress:
                    download_task = progress.add_task("Download", total=total)
                    for chunk in resp.iter_bytes():
                        out_file.write(chunk)
                        progress.update(download_task, completed=resp.num_bytes_downloaded)

