# coding:utf-8
# !/usr/bin/env python
import os
import socket
import time

from bs4 import BeautifulSoup

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
proxy_dir = os.path.join(PROJECT_ROOT, 'static/proxy/proxies.txt')


class Proxy:
    def __init__(self):
        self.proxy_list = []
        self.proxy_filter_list = []

    def get_proxy(self):
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = dict()
        header['User-Agent'] = User_Agent

        for i in range(1, 2):
            time.sleep(1)
            url = 'http://www.xicidaili.com/nn/' + str(i)
            res = requests.get(url=url, headers=header).content

            soup = BeautifulSoup(res, "html.parser")
            ips = soup.findAll('tr')

            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                print(ip_temp)
                self.proxy_list.append(ip_temp)

    def filter_proxy(self):
        socket.setdefaulttimeout(1)
        f = open(proxy_dir, "w")
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Connection': 'keep-alive'}
        url = "http://icanhazip.com"
        proxy_num = 0
        for proxy in self.proxy_list:
            proxy_temp = {"https": "https://{}".format(proxy)}
            try:
                req = requests.get(url, proxies=proxy_temp, timeout=2, headers=head).content
                # print(req)
                write_proxy = proxy + "\n"
                f.write(write_proxy)
                proxy_num += 1
            except Exception:
                # print ("代理链接超时，去除此IP：{0}".format(proxy))
                continue

                # print("总共可使用ip量为{}个".format(proxy_num))

    def main(self):
        self.get_proxy()
        self.filter_proxy()

    def get_filter_proxy_list(self):
        with open(proxy_dir, "r") as f:
            lins = f.readlines()
            for i in lins:
                p = i.strip("\n")
                self.proxy_filter_list.append(p)
            return self.proxy_filter_list

    def get_filter_proxy(self):
        ip = self.get_filter_proxy_list()
        setIp = ip[random.randint(0, len(ip) - 1)]
        proxy = {
            'http': 'http://{}'.format(setIp),
            'https': 'http://{}'.format(setIp),
        }
        return proxy


import requests
import random
from bs4 import BeautifulSoup as bs

sess = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def gain_ip_port():
    response = sess.get('http://www.xicidaili.com/wt/', headers=headers)
    response.encoding = response.apparent_encoding
    # print(response.text)
    soup = bs(response.text, 'html.parser')
    table = soup.find('table', {'id': 'ip_list'})
    trs = table.find_all('tr')[1:]
    ip_list = []
    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[1].string
        port = tds[2].string
        ip_list.append(ip + ':' + port)
    return ip_list


def checkout_valid(ip):
    try:
        html = sess.get('http://www.baidu.com', proxies={'http': ip}, headers=headers)
        return html.status_code == 200
    except Exception as e:
        return False


def get_proxy():
    ip_pool = gain_ip_port()
    url = 'http://www.whatismyip.com/'
    proxies = {
        'http': ''
    }
    ip = random.choice(ip_pool)
    while not checkout_valid(ip):
        ip_pool.remove(ip)
        ip = random.choice(ip_pool)

    proxies['http'] = ip
    response = sess.get(
        url,
        proxies=proxies,
        headers=headers
    )
    response.encoding = response.apparent_encoding
    print(response.text)


def main():
    proxy = Proxy()
    # proxy.main()
    print proxy.get_filter_proxy_list()


if __name__ == '__main__':
    main()
