import aiohttp
import asyncio
import os
import requests
import PIL
from PIL import Image
import io
from datetime import datetime
import time
import logging

address='http://142.93.138.114/images/'

async def downloadFromServer(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            filename = os.path.basename(url)
            with open(filename, 'wb') as f_handle:
                while True:
                    chunk = await response.content.read()
                    if not chunk:
                        logging.info(u'Finished downloading {filename}'.format(filename=url))
                        break
                    im = Image.open(io.BytesIO(chunk))
                    ready = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                    buf = io.BytesIO()
                    ready.save(buf, format= "JPEG")
                    ready.save(filename,format="JPEG")
                    reflect(url, buf)
        await response.release()
        return filename


async def reflect(url, buf):
    files = {url: io.BytesIO(buf.getvalue())}
    rr = requests.post(address, files=files)


def download():
    urls = []
    res = requests.get(address).content.decode('utf-8').split()
    for i in res:
        urls.append(address + i)

    loop = asyncio.get_event_loop()
    process_download = asyncio.gather(*[downloadFromServer(url) for url in
                                        urls])
    results = loop.run_until_complete(process_download)
    loop.close()


def main():
    logging.basicConfig(level=logging.DEBUG)
    download()


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    print(datetime.now() - start_time)
