#!/usr/bin/python
# coding=utf8

from collections import OrderedDict

import requests

__author__ = 'Jam'
__date__ = '2019/1/11 14:53'


def _set_header_default():
    header_dict = OrderedDict()
    header_dict["Accept"] = "application/json, text/plain, */*"
    header_dict["Accept-Encoding"] = "gzip, deflate"
    header_dict["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
    header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    return header_dict


class HTTPClient(object):
    def __init__(self):
        self.init_session()

    def init_session(self):
        self._s = requests.Session()
        self._s.headers.update(_set_header_default())
        return self

    def set_cookies(self, **kwargs):
        for k, v in kwargs.items():
            self._s.cookies.set(k, v)

    def get_cookies(self):
        return self._s.cookies.values()

    def del_cookies(self):
        self._s.cookies.clear()

    def del_cookies_by_key(self, key):
        self._s.cookies.set(key, None)

    def set_headers(self, headers):
        self._s.headers.update(headers)
        return self

    def reset_headers(self):
        self._s.headers.clear()
        self._s.headers.update(_set_header_default())

    def get_headers_host(self):
        return self._s.headers["Host"]

    def set_headers_host(self, host):
        self._s.headers.update({"Host": host})
        return self

    def get_headers_referer(self):
        return self._s.headers["Referer"]

    def set_headers_referer(self, referer):
        self._s.headers.update({"Referer": referer})
        return self
