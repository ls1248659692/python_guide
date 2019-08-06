#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/7/26 11:42'

import pandas as pd

link = 'http://pandas.pydata.org/pandas-docs/version/0.20/io.html'

df1 = pd.read_html(link)[0]
print(df1)
print(df1.to_html('df1.html'))