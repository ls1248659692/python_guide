#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/6/5 17:33'

import sys

from colorama import init
from pyfiglet import figlet_format
from termcolor import cprint

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
cprint(figlet_format('Python'))
