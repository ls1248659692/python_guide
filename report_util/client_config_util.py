#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/6/5 16:38'

import json


class Config(object):
    def __init__(self, config_dict):
        self.data = config_dict


class ClientConfig(Config):
    def __init__(self, json_config_file):
        with open(json_config_file) as fh:
            data = json.load(fh)
        super(ClientConfig, self).__init__(data)
