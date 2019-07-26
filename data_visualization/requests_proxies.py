#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/5/14 15:33'

import requests


def check_ip_proxy():
    proxies = {
        'http': 'http://proxy.capvision.com:8080',
        'https': 'http://proxy.capvision.com:8080'
    }

    url = 'http://icanhazip.com/'  # check ip
    response = requests.get(url, proxies=proxies, verify=False)  # do not need ssl verify
    print  'proxy_ip:', response.text.strip()

    response = requests.get(url)
    print  'local_ip:', response.text.strip()


def main():
    check_ip_proxy()


if __name__ == '__main__':
    main()
