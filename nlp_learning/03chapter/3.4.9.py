# coding:utf-8
'''
皮尔逊相关系数的Python实现
author：白宁超
site：http://www.cnblogs.com/baiboy/
'''
import numpy as np
vec1 = np.array([1,2,3,4])
vec2 = np.array([5,6,7,8])


#方法一：根据公式求解
vec1_=vec1-np.mean(vec1)
vec2_=vec2-np.mean(vec2)
dist1=np.dot(vec1_,vec2_)/(np.linalg.norm(vec1_)*np.linalg.norm(vec2_))
print("皮尔逊相关系数测试结果是：\t"+str(dist1))

#方法二：根据numpy库求解
Vec=np.vstack([vec1,vec2])
dist2=np.corrcoef(Vec)[0][1]
print("皮尔逊相关系数测试结果是：\t"+str(dist2))