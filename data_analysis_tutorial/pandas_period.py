#!/usr/bin/python
# coding=utf8
import numpy as np
import pandas as pd

__author__ = 'Jam'
__date__ = '2019/6/4 15:20'

# 时间戳与时期之间的转换：pd.to_period()、pd.to_timestamp()

rng = pd.date_range('2017/1/1', periods=10, freq='M')
prng = pd.period_range('2017', '2018', freq='M')

ts1 = pd.Series(np.random.rand(len(rng)), index=rng)
print("1".center(40, '*'))
print(ts1.head())
print("2".center(40, '*'))
print(ts1.to_period().head())
# 每月最后一日，转化为每月

ts2 = pd.Series(np.random.rand(len(prng)), index=prng)
print("3".center(40, '*'))
print(ts2.head())
print("4".center(40, '*'))
print(ts2.to_timestamp().head())

