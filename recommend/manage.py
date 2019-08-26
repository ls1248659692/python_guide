#!/usr/bin/python
# coding=utf8
import sys

from preprocess import run as pre_process
from workflow.cf_workflow import run as user_cf
from workflow.lfm_workflow import run as lfm
from workflow.personal_rank_workflow import run as personal_rank

__author__ = 'Jam'
__date__ = '2019/6/18 11:27'


def manage():
    arg = sys.argv[1]

    if arg == 'pre_process':
        pre_process()
    elif arg == 'cf':
        user_cf()
    elif arg == 'lfm':
        lfm()
    elif arg == 'personal_rank':
        personal_rank()
    else:
        raise ValueError('Args must in ["pre_process", "cf", "lfm", "personal_rank"].')

    sys.exit(0)


if __name__ == '__main__':
    manage()
