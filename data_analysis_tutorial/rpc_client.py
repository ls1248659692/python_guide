#!/usr/bin/python
# coding=utf8

import xmlrpc.client
from xmlrpc.client import ServerProxy

__author__ = 'Jam'
__date__ = '2019/6/26 18:07'

if __name__ == '__main__':
    server = ServerProxy("http://localhost:8888", allow_none=True)
    print (server.get_string("cloudox"))
    print (server.add(8, 8))

    # 上传文件
    put_handle = open("./tmp/pd_figure_0.png", 'rb')
    server.image_put(xmlrpc.client.Binary(put_handle.read()))
    put_handle.close()

    # 下载文件
    get_handle = open("./tmp/test.png", 'wb')
    get_handle.write(server.image_get().data)
    get_handle.close()
