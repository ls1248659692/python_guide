#!/usr/bin/python
# coding=utf8
import requests
from jsonrpc.proxy import ServiceProxy

__author__ = 'Jam'
__date__ = '2019/6/26 14:50'


def get_rpc_call():
    server = ServiceProxy('http://txtvoice.capvision.com/jsonrpc/')
    res = server.callback.user('admin', 'asdf1234!', 'RPC')
    print res


def get_request_call():
    params = {
        'username': 'admin',
        'password': 'asdf1234!',
        'arg': 'rpc'
    }
    result = requests.get(
        'http://txtvoice.capvision.com/jsonrpc/callback.user/?',
        params=params
    )
    print result.content


def main():
    get_rpc_call()
    get_request_call()


if __name__ == '__main__':
    main()
