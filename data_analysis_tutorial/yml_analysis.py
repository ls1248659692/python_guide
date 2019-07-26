#!/usr/bin/python
# coding=utf8
import json

import yaml

__author__ = 'Jam'
__date__ = '2019/4/22 14:12'


def check_yml():
    yml_str = """
    root:
      user:
        name: Jam
        sex: man
      company:
        - floor: 10
        - number: 9527
        - depends_on:
          - capvision
          - baidu
      site:
        - shanghai
        - wuhan
        - chengdu
        - hangzhou
    """

    yml_data = yaml.load(yml_str)
    return yml_data


class YamlAnalysis(object):
    def __init__(self):
        self.data = None

    def get_config(self):
        with open('./data/config.yml', 'r') as f:
            yml_data = f.read()

            self.data = yaml.load(yml_data)
        return self.data


class InitExample:
    name = 'Gxs'

    def __init__(self, name, height, weight):
        self.name = name
        self.height = height
        self.weight = weight


def main():
    yml_str = check_yml()
    yml_config = YamlAnalysis().get_config()
    print type(yml_str), type(yml_config)

    print json.dumps(yml_str, indent=4, sort_keys=True)
    print json.dumps(yml_config, indent=4, sort_keys=True)

    init_example = InitExample('Jam', 180, 18)
    print InitExample.name
    print init_example.name
    print init_example.height
    print init_example.weight


if __name__ == '__main__':
    main()
