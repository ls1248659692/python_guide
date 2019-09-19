# coding:utf-8
# !/usr/bin/env python

import subprocess
import glob

import six


def auto_run():
    tests = sorted(glob.glob('[A-Za-z]*.py'))
    excludes = ['runtests.py']

    for test in tests:
        if test not in excludes:
            six.print_('%s ...' % test)
            subprocess.call(['python', './%s' % test])

    six.print_('Done.')


def main():
    auto_run()
    pass


if __name__ == '__main__':
    main()
