# coding:utf-8
'''
杰卡德距离的Python实现
author：白宁超
site：http://www.cnblogs.com/baiboy/
'''
import numpy as np
# v1 = np.mat([1,2,3,4]) > 0.5
# v2 = np.mat([5,6,7,8]) > 0.5

v1=np.random.random(10)>0.5
v2=np.random.random(10)>0.5


vec1=np.asarray(v1,np.int32)
vec2=np.asarray(v2,np.int32)

#方法一：根据公式求解
up=np.double(np.bitwise_and((vec1 != vec2),np.bitwise_or(vec1 != 0, vec2 != 0)).sum())
down=np.double(np.bitwise_or(vec1 != 0, vec2 != 0).sum())
dist1=(up/down)
print("杰卡德距离测试结果是：\t"+str(dist1))

#方法二：根据scipy库求解
from scipy.spatial.distance import pdist
Vec=np.vstack([vec1,vec2])
dist2=pdist(Vec,'jaccard')
print("杰卡德距离测试结果是：\t"+str(dist2))