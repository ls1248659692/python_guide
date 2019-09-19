#!/usr/bin/python
# coding=utf8
import random

__author__ = 'Jam'
__date__ = '2018/11/26 9:57'


def random_choice_str(randomlength=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789!@#$%^&*()_+=-'

    random_str_list = random.sample(chars, randomlength)

    return ''.join(random_str_list)

def return_link(link_url,description):
    return "<a href=\"%s\">%s</a>" % (link_url,description)

if __name__ == '__main__':
    print random_choice_str()
    print return_link('www.baidu.com', u'测试百度页面')
