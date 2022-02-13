# coding:utf-8
'''
曼哈顿距离的Python实现
author：白宁超
site：http://www.cnblogs.com/baiboy/
'''
import numpy as np
vec1 = np.mat([1,2,3,4])
vec2 = np.mat([5,6,7,8])

#方法一：根据公式求解
dist1=np.sum(np.abs(vec1-vec2))
print("曼哈顿距离测试结果是：\t"+str(dist1))

#方法二：根据scipy库求解
from scipy.spatial.distance import pdist
Vec=np.vstack([vec1,vec2])
dist2=pdist(Vec,'cityblock')
print("曼哈顿距离测试结果是：\t"+str(dist2))

from numpy import *
dist3 = sum(abs(vec1-vec2))
print("曼哈顿距离测试结果是：\t"+str(dist3))