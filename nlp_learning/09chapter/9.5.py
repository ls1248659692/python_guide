# from __future__ import unicode_literals
# import sys
# sys.path.append("../")

import jieba
import jieba.posseg
import jieba.analyse

print('='*40)
print('1. 分词')
print('-'*40)

prpaStr="我来到北京清华大学,看到让我蓝瘦香菇的word哥，真是让人无语。"
seg_list = jieba.cut(prpaStr, cut_all=True)
print("全模式分词: \n" + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut(prpaStr, cut_all=False)
print("默认模式分词: \n" + "/ ".join(seg_list))  # 默认模式

seg_list = jieba.cut(prpaStr)
print("自定义分隔符分词：\n"+",".join(seg_list))

seg_list = jieba.cut_for_search(prpaStr)  # 搜索引擎模式
print("搜索引擎模式：\n"+",".join(seg_list))




print("\n"*5+'='*40)
print('2. 添加自定义词典/调整词典')
print('-'*40)

prpaStr1 = '如果放到post中将出错。'
print("未调整词典的分词：\n"+'/'.join(jieba.cut(prpaStr1, HMM=False)))
print(jieba.suggest_freq(('中', '将'), True))
print("调整词典的分词：\n"+'/'.join(jieba.cut(prpaStr1, HMM=False)))

prpaStr2 = '「台中」正确应该不会被切开'
print("未调整词典的分词：\n"+'/'.join(jieba.cut(prpaStr2, HMM=False)))
print(jieba.suggest_freq('台中', True))
print("调整词典的分词：\n"+'/'.join(jieba.cut(prpaStr2, HMM=False)))




print("\n"*5+'='*40)
print('3. 关键词提取')
print('-'*40)
prpaStr3 = "此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。目前在建吉林欧亚城市商业综合体项目。2013年，实现营业收入0万元，实现净利润-139.13万元。"

print('3.1 TF-IDF关键词提取法：\n')
for word, weight in jieba.analyse.extract_tags(prpaStr3, withWeight=True):
    print('%s %s' % (word, weight))

print('3.2 TextRank关键词提取法：\n')
for word, weight in jieba.analyse.textrank(prpaStr3, withWeight=True):
    print('%s %s' % (word, weight))




print("\n"*5+'='*40)
print('4. 词性标注')
print('-'*40)

words = jieba.posseg.cut(prpaStr)
for word, flag in words:
    print('%s %s' % (word, flag))




print("\n"*5+'='*40)
print('5. Tokenize: 返回词语在原文的起止位置')
print('-'*40)

print('5.1 默认模式\n')
prpaStr4 = '永和服装饰品有限公司'
result = jieba.tokenize(prpaStr4)
for tk in result:
    print("word: %s\t start: %d \t end: %d" % (tk[0],tk[1],tk[2]))

print('5.2 搜索模式\n')
result = jieba.tokenize(prpaStr4, mode='search')
for tk in result:
    print("word: %s\t start: %d \t end:%d" % (tk[0],tk[1],tk[2]))