#!/usr/bin/python
# coding=utf8
import json
import re
import time
import traceback
from functools import wraps

import concurrent.futures
import requests

__author__ = 'Jam'
__date__ = '2019/6/5 17:03'


def encode_to_dict(encoded_str):
    pair_list = encoded_str.split('&')
    pair_dict = {}
    for pair in pair_list:
        if pair:
            key = pair.split('=')[0]
            val = pair.split('=')[1]
            pair_dict[key] = val
    return pair_dict


def parse_curl_str(s):
    pat = re.compile("'(.*?)'")
    str_list = [i.strip() for i in re.split(pat, s)]

    url = ''
    headers_dict = {}
    data = ''

    for i in range(0, len(str_list) - 1, 2):
        arg = str_list[i]
        string = str_list[i + 1]

        if arg.startswith('curl'):
            url = string

        elif arg.startswith('-H'):
            header_key = string.split(':', 1)[0].strip()
            header_val = string.split(':', 1)[1].strip()
            headers_dict[header_key] = header_val

        elif arg.startswith('--data'):
            data = string

    return url, headers_dict, data


def retry(retries=3, interval=1):
    def _retry(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            index = 0
            response = None
            while index < retries:
                index += 1
                try:
                    response = func(*args, **kwargs)
                    if response.status_code == 404:
                        print(404)
                        break
                    elif response.status_code != 200:
                        print(response.status_code)
                        time.sleep(interval)
                        continue
                    else:
                        break
                except BaseException:
                    traceback.print_exc()

            return response

        return _wrapper

    return _retry


def my_ip():
    ip_dict = json.loads(
        requests.get(
            'https://api.ipify.org?format=json'
        ).text
    )

    return ip_dict['ip']


def form_data_to_dict(s):
    arg_list = [line.strip() for line in s.split('\n')]
    d = {}
    for i in arg_list:
        if i:
            k = i.split(':', 1)[0].strip()
            v = ''.join(i.split(':', 1)[1:]).strip()
            d[k] = v
    return d


class ThreadPoolCrawler(object):
    def __init__(self, urls, concurrency=10):
        self.urls = urls
        self.concurrency = concurrency
        self.results = []

    def handle_response(self, url, response):
        pass

    def get(self, url):
        return requests.get(url)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            future_to_url = {
                executor.submit(self.get, url): url for url in self.urls
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    response = future.result()
                except Exception as e:
                    traceback.print_exc()
                else:
                    self.handle_response(url, response)


class TestCrawler(ThreadPoolCrawler):
    def handle_response(self, url, response):
        print url, response.text

    @staticmethod
    def start_request():
        urls = ['https://api.ipify.org/?format=json'] * 20
        for nums in [2, 5, 10, 15, 20]:
            beg = time.time()
            s = TestCrawler(urls, nums)
            s.run()
            print(nums, time.time() - beg)


def unit_test():
    pass
    # encode_to_dict('name=foo&val=bar')
    # my_ip()
    TestCrawler.start_request()


if __name__ == '__main__':
    unit_test()
