#!/usr/bin/python
# coding=utf8
import asyncio
import time

import aiohttp
import requests

__author__ = 'Jam'
__date__ = '2019/7/5 17:33'


def job(t):
    print('Start job ', t)
    time.sleep(t)
    print('Job ', t, ' takes ', t, ' s')


def main():
    [job(t) for t in range(1, 10)]


t1 = time.time()
main()
print("NO async total time : ", time.time() - t1)
print('*1*'.center(50, '-'))


async def job(t):
    print('Start job ', t)
    await asyncio.sleep(t)
    print('Job ', t, ' takes ', t, ' s')


async def main(loop):
    tasks = [loop.create_task(job(t)) for t in range(1, 10)]
    await asyncio.wait(tasks)


t1 = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
print("Async total time : ", time.time() - t1)
print('*2*'.center(50, '-'))

URL = 'https://morvanzhou.github.io/'


def normal():
    for i in range(2):
        r = requests.get(URL)
        url = r.url
        print(url)


t1 = time.time()
normal()
print("Normal total time:", time.time() - t1)
print('*3*'.center(50, '-'))


async def job(session):
    response = await session.get(URL)
    return str(response.url)


async def normal_main(loop):
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(job(session)) for _ in range(2)]
        finished, unfinished = await asyncio.wait(tasks)
        all_results = [r.result() for r in finished]
        print(all_results)


t1 = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(normal_main(loop))
loop.close()
print("Async total time:", time.time() - t1)
print('*4*'.center(50, '-'))
