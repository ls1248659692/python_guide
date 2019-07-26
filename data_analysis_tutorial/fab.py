#!/usr/bin/python
# coding=utf8
'''
pip install fabric==1.1

attention: fabric need run in cmd
cd data_analysis_tutorial
fab -f fab_ops.py go
'''
__author__ = 'Jam'
__date__ = '2019/5/18 15:13'

from fabric.api import *

env.hosts = ['192.168.5.141', ]
env.port = '22'
env.user = 'root'
env.password = 'abc@123'


def remote_host():
    run('ls -l')


def lsfab():
    with cd('/tmp/'):
        run('ls')


def host_name():
    run('uname -s')


@task
def go():
    lsfab()
    host_name()
    remote_host()
