# coding:utf-8
# !/usr/bin/env python

import importlib

packages = ['pandas', 'IPython', 'statsmodels', 'sklearn', 'seaborn',
            'toolz', 'bs4', 'requests', 'scipy', 'tables']

fail_packages = []
for package in packages:
    try:
        importlib.import_module(package)
    except ImportError:
        fail_packages.append("can't import %s" % package)
else:
    if len(fail_packages) > 0:
        print('package don\'t install: ' + ','.join(fail_packages))
    else:
        print('packages pip install ok.')
