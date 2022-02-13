#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jieba
import os
import re
import time
from jpype import *

'''
title：利用结巴分词进行文本语料的批量处理
    1 首先对文本进行遍历查找
    2 创建原始文本的保存结构
    3 对原文本进行结巴分词和停用词处理
    4 对预处理结果进行标准化格式，并保存原文件结构路径
author：白宁超
myblog：http://www.cnblogs.com/baiboy/
'''


'''
创建文件目录
path:根目录下创建子目录
'''
def mkdir(path):
    # 判断路径是否存在
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        print(path+' 创建成功')
        return True
    else:
        pass
    print('-->请稍后，文本正在预处理中...')


'''
结巴分词工具进行中文分词处理：
read_folder_path：待处理的原始语料根路径
write_folder_path 中文分词经数据清洗后的语料
'''
def CHSegment(read_folder_path,write_folder_path):
    stopwords ={}.fromkeys([line.strip() for line in open('../Database/stopwords/CH_stopWords.txt','r',encoding='utf-8')]) # 停用词表
    # 获取待处理根目录下的所有类别
    folder_list = os.listdir(read_folder_path)
    # 类间循环
    # print(folder_list)
    for folder in folder_list:
        #某类下的路径
        new_folder_path = os.path.join(read_folder_path, folder)
        # 创建一致的保存文件路径
        mkdir(write_folder_path+folder)
         #某类下的保存路径
        save_folder_path = os.path.join(write_folder_path, folder)
        #某类下的全部文件集
        # 类内循环
        files = os.listdir(new_folder_path)
        j = 1
        for file in files:
            if j > len(files):
                break
            # 读取原始语料
            raw = open(os.path.join(new_folder_path, file),'r',encoding='utf-8').read()
            # 只保留汉字
            # raw1 = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", raw)
            # jieba分词
            wordslist = jieba.cut(raw, cut_all=False) # 精确模式
            # 停用词处理
            cutwordlist=''
            for word in wordslist:
                if word not in stopwords and word=="\n":
                    cutwordlist+="\n" # 保持原有文本换行格式
                elif len(word)>1 :
                        cutwordlist+=word+"/" #去除空格
            #保存清洗后的数据
            with open(os.path.join(save_folder_path,file),'w',encoding='utf-8') as f:
                f.write(cutwordlist)
                j += 1


'''
结巴分词工具进行中文分词处理：
read_folder_path：待处理的原始语料根路径
write_folder_path 中文分词经数据清洗后的语料
'''
def HanLPSeg(read_folder_path,write_folder_path):
    startJVM(getDefaultJVMPath(), "-Djava.class.path=C:\hanlp\hanlp-1.3.2.jar;C:\hanlp", "-Xms1g", "-Xmx1g") # 启动JVM，Linux需替换分号;为冒号:
    stopwords ={}.fromkeys([line.strip() for line in open('../MLThorMethod/09chapter/NLPIR_stopwords.txt','r',encoding='utf-8')]) # 停用词表
    # 获取待处理根目录下的所有类别
    folder_list = os.listdir(read_folder_path)
    # 类间循环
    # print(folder_list)
    for folder in folder_list:
        #某类下的路径
        new_folder_path = os.path.join(read_folder_path, folder)
        # 创建一致的保存文件路径
        mkdir(write_folder_path+folder)
         #某类下的保存路径
        save_folder_path = os.path.join(write_folder_path, folder)
        #某类下的全部文件集
        # 类内循环
        files = os.listdir(new_folder_path)
        j = 1
        for file in files:
            if j > len(files):
                break
            # 读取原始语料
            raw = open(os.path.join(new_folder_path, file),'r',encoding='utf-8').read()
            # HanLP分词
            HanLP = JClass('com.hankcs.hanlp.HanLP')
            wordslist = HanLP.segment(raw)
            #保存清洗后的数据
            wordslist1=str(wordslist).split(",")
            # print(wordslist1[1:len(wordslist1)-1])

            flagresult=""
            # 去除标签
            for v in wordslist1[1:len(wordslist1)-1]:
                if "/" in v:
                    slope=v.index("/")
                    letter=v[1:slope]
                    if len(letter)>0 and '\n\u3000\u3000' in letter:
                        flagresult+="\n"
                    else:flagresult+=letter +"/" #去除空格
            # print(flagresult)
            with open(os.path.join(save_folder_path,file),'w',encoding='utf-8') as f:
                f.write(flagresult.replace(' /',''))
            j += 1
    shutdownJVM()

if __name__ == '__main__' :
    # 运行错误时候，读者修改下文件路径即可
    print('开始进行文本分词操作：\n')
    t1 = time.time()

    dealpath="../Database/SogouC/FileTest/"
    savepath="../Database/SogouCCut/FileTest/"

    # 待分词的语料类别集根目录
    read_folder_path = '../Database/SogouC/FileNews/'
    write_folder_path = '../Database/SogouCCut/'

    #jieba中文分词
    CHSegment(read_folder_path,write_folder_path) #300个txtq其中结巴分词使用3.31秒
    HanLPSeg(read_folder_path,write_folder_path) #300个txt其中hanlp分词使用1.83秒

    t2 = time.time()
    print('完成中文文本切分: '+str(t2-t1)+"秒。")
