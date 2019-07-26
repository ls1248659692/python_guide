#!/usr/bin/python
# coding=utf8
from __future__ import with_statement

from fabric.context_managers import lcd
from fabric.operations import local

__author__ = 'Jam'
__date__ = '2019/5/29 15:09'


def update():
    local("sudo apt-get update")


def git():
    local("sudo apt-get install git")
    local("git config --global user.name 'Pasquali'")
    local("git config --global user.email 'pasaquali@gmail.com'")


def python():
    local("sudo apt-get install python")


def setup_tools():
    local("sudo apt-get install python-setuptools")


def pip():
    local("sudo apt-get install python-pip python-dev build-essential -y")


def create_virtual():
    local("sudo pip install virtualenv virtualenvwrapper")
    bashrc_dir = '..'
    with lcd(bashrc_dir):
        local("echo 'export WORKON_HOME=~/.virtualenvs' >> .bashrc")
        local("echo '. /usr/local/bin/virtualenvwrapper.sh' >> .bashrc")


def edit_vimrc():
    vimrc_file = '..'
    with lcd(vimrc_file):
        local("git clone https://github.com/amix/vimrc.git ~/.vim_runtime")
        local("sh ~/.vim_runtime/install_awesome_vimrc.sh")


def messages():
    local("echo '. ~/.bashrc'")
    local("")
    local("echo do not forget to begin a virtualenv before starting part 2")
    local("")
    local("echo do not forget to edit vim.rc")
