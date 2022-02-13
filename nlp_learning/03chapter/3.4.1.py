# coding:utf-8
'''
夹角余弦距离的Python实现
author：白宁超
site：http://www.cnblogs.com/baiboy/
'''
import numpy as np
vec1 = [1,2,3,4]
vec2 = [5,6,7,8]

#方法一：根据公式求解
dist1=np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
print("余弦距离测试结果是：\t"+str(dist1))

#方法二：根据scipy库求解
from scipy.spatial.distance import pdist
Vec=np.vstack([vec1,vec2])
dist2=1-pdist(Vec,'cosine')
print("余弦距离测试结果是：\t"+str(dist2))

