#!/usr/bin/python
# coding=utf8

from SimpleXMLRPCServer import SimpleXMLRPCServer

import xmlrpc.client
from socketserver import ThreadingMixIn

__author__ = 'Jam'
__date__ = '2019/6/26 18:12'


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def respon_string(str):
    return "get string:%s" % str


def add(x, y):
    return x + y


def image_get():
    handle = open("./data/test.png", 'rb')
    return xmlrpc.client.Binary(handle.read())


def image_put(data):
    handle = open("./data/pd_figure_0.png", 'wb')
    handle.write(data.data)
    handle.close()


if __name__ == '__main__':
    server = ThreadXMLRPCServer(('localhost', 8888), allow_none=True)

    # Call Mapping
    server.register_function(respon_string, "get_string")
    server.register_function(add, 'add')
    server.register_function(image_put, 'image_put')
    server.register_function(image_get, 'image_get')

    print ("Listening for Client")
    server.serve_forever()
