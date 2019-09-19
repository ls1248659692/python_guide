# coding:utf-8
# !/usr/bin/env python

import socket
import time


def get_ip():
    is_develop = False
    item_list = socket.gethostbyname_ex(socket.gethostname())
    print item_list

    for ipList in item_list:
        if isinstance(ipList, list) and ipList is not None:
            for ip in ipList:
                if ip.startswith('192.168.50'):
                    is_develop = True
                    print 'The current {ip}  is develop environment.'.format(ip=ip)
                elif ip.startswith('192.168.5'):
                    is_develop = False
                    print 'The current {ip}  is not develop environment.'.format(ip=ip)

    return is_develop


def retry_run():
    retryTimes = 5
    while retryTimes > 0:
        try:
            return get_ip()
        except BaseException:
            print '.',
            retryTimes -= 1


def main():
    retry_times = 5
    while retry_times:
        try:
            result = get_ip()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print e
            retry_times -= 1
        finally:
            print 'sleep 1 second'
            time.sleep(1)
            retry_times -= 1


if __name__ == '__main__':
    main()
