#!/usr/bin/python
# coding=utf8
from warnings import filterwarnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql
import seaborn as sns

__author__ = 'Jam'
__date__ = '2018/11/27 15:39'

## DB ignore waring
filterwarnings('ignore', category=pymysql.Warning)

# speed pandas
# import modin.pandas as pd

## pd.setting
islc = pd.IndexSlice
pd.options.display.float_format = '{:,.2f}'.format
pd.options.mode.chained_assignment = None
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option("display.max_rows", 9999)
pd.set_option('display.max_columns', 9999)
pd.set_option('display.width', 9999)
pd.set_option('max_colwidth', 9999)
pd.set_option('precision', 2)

## np.setting
np.set_printoptions(threshold=np.inf)

## sns.setting
sns.set_style('whitegrid', {'font.sans-serif': ['simhei', 'Arial']})

## plt.setting
plt.rcParams['font.sans-serif'] = ['simhei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams["axes.labelsize"] = 16
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 12
plt.rcParams["figure.figsize"] = [14, 10]