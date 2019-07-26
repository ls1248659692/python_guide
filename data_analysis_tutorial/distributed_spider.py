#!/usr/bin/python
# coding=utf8
import multiprocessing as mp
import re
import time
from urllib import urlopen

from bs4 import BeautifulSoup
from future.backports.urllib.parse import urljoin

__author__ = 'Jam'
__date__ = '2019/7/5 17:03'

base_url = 'https://morvanzhou.github.io/'


def crawl(url):
    response = urlopen(url)
    time.sleep(1)
    return response.read().decode('utf-8', 'ignore')


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {"href": re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()

    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    url = soup.find('meta', {'property': "og:url"})['content']

    return title, page_urls, url


def run():
    unseen, seen = set(), set()
    unseen.add(base_url)

    pool = mp.Pool(4)
    start = time.time()

    while len(unseen) > 0:
        if len(seen) > 20:
            break

        print('Distributed Crawling...')
        crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
        htmls = [job.get() for job in crawl_jobs]

        print('Distributed Parsing...')
        parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
        results = [job.get() for job in parse_jobs]

        print('Distributed Saving...')
        seen.update(unseen)
        unseen.clear()

        for title, page_urls, url in results:
            print(title, url)
            unseen.update(page_urls - seen)

    print('Total time: %.1f s' % (time.time() - start,))


if __name__ == '__main__':
    run()
