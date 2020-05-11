import aiohttp
import asyncio
import json
import os
from bs4 import BeautifulSoup

STORAGE_ADDRESS="http://{address}:{port}/{api}".format(
    address=os.getenv("STORAGE_SERVICE_NAME"),
    port=os.getenv("STORAGE_SERVICE_PORT"),
    api="api/v1/content/"
)

SOURCE_ADDRESS="{}".format(os.getenv("CRAWLER_SOURCE_ADDRESS"))


async def fetch(session, url):
    async with session.get(url) as response:
        page = await response.read()
        async for content in crawle(BeautifulSoup(page, 'html.parser')):
            yield content


async def crawle(soup):
    for tag in soup.find_all("a", id="LinkArea:BoxOpLink"):
        name = tag.attrs.get("title", "Title missing")
        timestamp = tag.find("span", class_="o-article__timestamp is-new").string
        content = {'name': name, 'timestamp': timestamp}
        print("crawle: put: {}".format(content))
        yield content


async def send(session, content):
    try:
        await session.post(STORAGE_ADDRESS, json=json.dumps(content))
        print("send: {} sending...".format(content))
    except aiohttp.client_exceptions.ClientConnectorError:
        print("send: cannot establish connection")
    finally:
        await asyncio.sleep(1)


async def loop():
    async with aiohttp.ClientSession() as session:
        print(SOURCE_ADDRESS)
        async for content in fetch(session, SOURCE_ADDRESS):
            await send(session, content)


async def main():
    while True:
        await loop()
        await asyncio.sleep(10 * 60) # 10 minutes


if __name__ == '__main__':
    asyncio.run(main())