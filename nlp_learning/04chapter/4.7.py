补充熵的运算
"""
计算信息熵
"""
from collections import Counter
from math import log
from decimal import Decimal

'''创建数据集，返回数据集和标签'''
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

'''计算数据集的香农熵(信息期望值):熵越高表示混合数据越多，度量数据集无序程度'''
def calcShannonEnt(dataSet):
    numEntries = len(dataSet) # 计算数据集中实例总数
    labelCounts = {} # 创建字典，计算分类标签label出现的次数
    for featVec in dataSet:
        currentLabel = featVec[-1] # 记录当前实例的标签
        if currentLabel not in labelCounts.keys():# 为所有可能的分类创建字典
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        # print(featVec, labelCounts) # 打印特征向量和字典的键值对

    # 对于label标签的占比，求出label标签的香农熵
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries # 计算类别出现的概率。
        shannonEnt -= prob * log(prob, 2) # 计算香农熵，以 2 为底求对数
    print('数据集的香农熵:',Decimal(shannonEnt).quantize(Decimal('0.00000')))
    return shannonEnt

if __name__=='__main__':
    dataSet, labels = createDataSet()
    calcShannonEnt(dataSet)
