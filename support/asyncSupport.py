import asyncio
import aiohttp
from sys import stderr
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)7s: %(message)s',
    stream=stderr,
)
log = logging.getLogger('')


# Support Functions
async def get(session, URLObj):
    async with session.get(URLObj['url'], headers=URLObj['headers']) as response:
        URLObj['data'] = await response.text() if (response.status == 200) else ''
        URLObj['status'] = response.status
        log.info("Reply status: {}".format(response.status))
        log.debug(response)


async def post(session, URLObj):
    async with session.post(URLObj['url'], headers=URLObj['headers'], data=URLObj['data']) as response:
        URLObj['data'] = await response.text() if (response.status == 200) else ''
        URLObj['status'] = response.status
        log.info("Reply status: {}".format(response.status))
        log.debug(response)

async def head(session, URLObj):
    async with session.head(URLObj['url'], headers=URLObj['headers'], data=URLObj['data']) as response:
        URLObj['data'] = await response.text() if (response.status == 200) else ''
        URLObj['status'] = response.status
        log.info("Reply status: {}".format(response.status))
        log.debug(response)

async def delete(session, URLObj):
    async with session.delete(URLObj['url'], headers=URLObj['headers'], data=URLObj['data']) as response:
        URLObj['data'] = await response.text() if (response.status == 200) else ''
        URLObj['status'] = response.status
        log.info("Reply status: {}".format(response.status))
        log.debug(response)


# Pass in a list of dictionaries of the form {'url':'some-url.whatever'}
# receive back a modified object of the form {'url':'some-url.whatever', 'data':'page data'}
async def batchGetURLs(URLList):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for URLObj in URLList:
            URLObj['data'] = '' # default to empty
            tasks.append( get(session, URLObj) )
        await asyncio.gather(*tasks)


async def batchPostURLs(URLList):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for URLObj in URLList:
            tasks.append( post(session, URLObj) )
        await asyncio.gather(*tasks)


async def batchHeadURLs(URLList):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for URLObj in URLList:
            URLObj['data'] = '' # default to empty
            tasks.append( head(session, URLObj) )
        await asyncio.gather(*tasks)


async def batchDeleteURLs(URLList):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for URLObj in URLList:
            URLObj['data'] = '' # default to empty
            tasks.append( delete(session, URLObj) )
        await asyncio.gather(*tasks)