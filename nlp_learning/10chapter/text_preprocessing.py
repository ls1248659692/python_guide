#!/usr/bin/env python
# coding:utf-8

"""
Author: Candymoon
Description: 通常在做文本挖掘建模的时候需要对文本进行预处理，其中几个主要的步骤如下:
    1. 高效的读取文本文件（保证内存不溢出）
    2. 处理文本的HTML标签、特殊符号（如微博文本）
    3. 分词去停用词
    4. 特征词选取并转换成文本特征向量
    5. 自定义规则提取特征词
Email: wenjun15182260944@163.com
Prompt: code in Python3 env
"""

'''-----------1. 高效的读取文本文件-------------------'''

import os

# 用生成器读取多个文件夹
class GeneratorReadFolders(object):
    def __init__(self, par_path):
        self.par_path = par_path

    def __iter__(self):  # 迭代器
        for file in os.listdir(self.par_path):
            file_abspath = os.path.join(self.par_path, file)
            if os.path.isdir(file_abspath):  # if file is a folder
                yield file_abspath  # use generator

# 用生成器读取多个文件夹
class GeneratorReadFiles(object):
    def __init__(self, par_path):
        self.par_path = par_path

    def __iter__(self):  # 迭代器
        folders = GeneratorReadFolders(self.par_path)
        for folder in folders:              # level directory
            # print("folder:", folder)
            catg = folder.split(os.sep)[-1]
            for file in os.listdir(folder):     # secondary directory
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    this_file = open(file_path, 'rb')  # 以rb读取方式文件 更快
                    content = this_file.read()
                    yield catg, file, content  # use generator
                    this_file.close()

'''-----------2. 处理文本的HTML标签、特殊符号（如微博文本）----------------'''

import re

# 过滤HTML中的标签
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 把script标签中的内容全部清除 added by candymoon
    rex = r'<script .*?>.*?</script>'
    dr = re.compile(rex, re.S)
    htmlstr = dr.sub('', htmlstr)
    # 先过滤CDATA
    re_cdata = re.compile('//<!CDATA\[[ >]∗ //\] > ', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    # style
    re_br = re.compile('<br\s*?/?>')
    # 处理换行
    re_h = re.compile('</?\w+[^>]*>')
    # HTML标签
    re_comment = re.compile('<!--[^>]*-->')
    # HTML注释
    s = re_cdata.sub('', htmlstr)
    # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)
    # 去掉style
    s = re_br.sub('', s)
    # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)
    # 去掉HTML注释
    re_comment1 = re.compile('<!--[^.*?]-->')
    s = re_comment1.sub('', s)
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('', s)

    blank_line_l = re.compile('\n')
    s = blank_line_l.sub('', s)

    blank_kon = re.compile('\t')
    s = blank_kon.sub('', s)

    blank_one = re.compile('\r\n')
    s = blank_one.sub('', s)

    blank_two = re.compile('\r')
    s = blank_two.sub('', s)

    blank_three = re.compile(' ')
    s = blank_three.sub('', s)

    http_link = re.compile(r'(http://.+.html)')
    s = http_link.sub('', s)

    s = replaceCharEntity(s)  # 替换实体
    return s

# 替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"''"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


# 清洗HTML标签文本
def extract(html_content, min_size = 10):
    try:
        html_content = ' '.join(html_content.split()) # 去掉多余的空格
        html_content = filter_tags(html_content)
        html_content = replaceCharEntity(html_content)
        html_content = ' '.join(html_content.split())  # 去掉多余的空格
        # print(len(html_content), html_content)
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')  # 判断是否包含中文
        match = zhPattern.search(html_content)
        if not match:
            return None
        if len(html_content) < min_size:
            return None
        return html_content
    except Exception as e:
        print(e)
        return None

#  微博数据清洗
def weibo_clear(weibo):
    rex = r'回复@\S+:'  # 格式：回复//@...:
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'//@\S+:'  # 格式：//@...:
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'@\S+ ?'  # 格式：@...空格
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'@\S+:?'  # 格式：@...:空格
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'#\S+#'  # 格式：#...#
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'null'  # 格式：null
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'【(.*?)】'  # 格式：【\S+】
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'我参与了发起的投票'  # 格式：我参与了...发起的投票
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'我分享了的文章'  # 格式：我分享了...的文章
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'我投给了“”这个选项。你也快来表态吧~'  # 格式：我投给了“...”这个选项。你也快来表态吧~
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'我发起了一个投票.*?网页链接'  # 格式：我发起了一个投票...网页链接
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'发表了博文'  # 格式：发表了博文
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'发表了一篇转载博文'  # 格式：发表了一篇转载博文
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r' http://\S+'  # 格式：http://
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'http://.*? '  # 格式：http://
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'查看详情：'  # 格式：查看详情：
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'转发微博 '  # 格式：转发微博
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'分享视频 '  # 格式：分享视频
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r' 网页链接'  # 格式： 网页链接
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'（记者.*?）'  # 格式：（记者 ...）
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'（图源见水印）'  # 格式：（图源见水印）
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'...展开全文c'  # 格式：...展开全文c
    dr = re.compile(rex, re.S)
    weibo = dr.sub('', weibo)

    rex = r'\[.*?\]'  # 格式：[...]
    dr = re.compile(rex, re.S)
    weibo = dr.sub(' ', weibo)

    rex = r'\|.*\... .*?\...'  # 格式：|xxx... xxx...
    dr = re.compile(rex, re.S)
    weibo = dr.sub(' ', weibo)

    rex = r'\|.*?\...'  # 格式：|xxx...
    dr = re.compile(rex, re.S)
    weibo = dr.sub(' ', weibo)

    return weibo

'''-----------3. 分词去停用词----------------'''

import jieba
import itertools

# 创建停用词列表
def createstoplist(stopwordspath):
    stwlist = [line.strip()
               for line in open(stopwordspath, 'r', encoding='utf-8').readlines()]
    return set(stwlist)

# 利用jieba对文本进行分词，返回切词后的list
def seg_doc(stwlist, str_doc):
    sent_list = str_doc.split('\n')  # 按行拆分
    sent_list = map(rm_char, sent_list)  # 去掉一些字符，例如\u3000
    word_2dlist = [rm_tokens(jieba.cut(part, cut_all=False), stwlist) for part in sent_list]  # 分词并去停用词
    word_list = list(itertools.chain(*word_2dlist))
    # word_list_str = ",".join(word_list)
    # print("word_list_str:", word_list_str)
    return word_list

# # 去掉一些停用词、数字、特殊符号
def rm_tokens(words, stwlist):
    words_list = list(words)
    for i in range(words_list.__len__())[::-1]:
        word = words_list[i]
        if word in stwlist:  # 去除停用词
            words_list.pop(i)
        elif word.isdigit():  # 去除数字
            words_list.pop(i)
        elif len(word) == 1:  # 去除单个字符
            words_list.pop(i)
        elif word == " ":  # 去除空字符
            words_list.pop(i)
    return words_list

# 替换特殊字符，如\u3000
def rm_char(text):
    text = re.sub('\u3000', '', text)
    return text

'''-----------4. 特征词选取并转换成文本向量----------------'''
import nltk

# 利用nltk进行词频特征统计
def nltk_wf_feature(word_list=None):
    # word_list参数样例数据如下：
    # word_list = ['我', '爱', '成都']
    wff = nltk.FreqDist(word_list)
    # 打印统计的词频
    for key in wff.keys():
        print(key, wff.get(key))

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# 利用sklearn计算tfidf值特征
def sklearn_tfidf_feature(corpus=None):

    # corpus参数样例数据如下：
    # corpus = ["我 来到 成都 春熙路",
    #           "今天 在 宽窄巷子 耍 了 一天 ",
    #           "成都 整体 来说 还是 挺 安逸 的",
    #           "成都 的 美食 真 巴适 惨 了"]
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])

from gensim import corpora, models
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np

# 利用gensim包进行特征词提取（推荐使用）
def gensim_feature(corpus=None):

    # corpus参数样例数据如下：
    # corpus = [["我", "来到", "成都", "春熙路"],
    #           ["今天", "在", "宽窄巷子", "耍", "了", "一天"],
    #           ["成都", "整体", "来说", "还是", "挺", "安逸", "的"],
    #           ["成都", "的", "美食", "真", "巴适", "惨", "了"]]
    dictionary = corpora.Dictionary(corpus)  # 构建语料词典

    # # 收集停用词和仅出现一次的词的id
    # stop_ids = [dictionary.token2id[stopword] for stopword in user_stop_word_list if stopword in dictionary.token2id]
    # once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    # dictionary.filter_tokens(stop_ids + once_ids) # 删除停用词和仅出现一次的词
    # dictionary.compactify()  # 消除id序列在删除词后产生的不连续的缺口
    # dictionary.save('mycorpus.dict')  # 把字典保存起来，方便以后使用

    # 统计词频特征
    dfs = dictionary.dfs  # 词频词典
    for key_id, c in dfs.items():
        print(dictionary[key_id], c)

    # 转换成doc_bow
    doc_bow_corpus = [dictionary.doc2bow(doc_cut) for doc_cut in corpus]

    # 生成tfidf特征
    tfidf_model = models.TfidfModel(dictionary=dictionary)  # 生成tfidf模型
    tfidf_corpus = [tfidf_model[doc_bow] for doc_bow in doc_bow_corpus]  # 将每doc_bow转换成对应的tfidf_doc向量

    # 生成lsi特征（潜在语义索引）
    lsi_model = models.LsiModel(corpus=tfidf_corpus, id2word=dictionary, num_topics=100)  # 生成lsi model
    # 生成corpus of lsi
    lsi_corpus = [lsi_model[tfidf_doc] for tfidf_doc in tfidf_corpus]  # 转换成lsi向量

    # 生成lda特征(主题模型)
    lda_model = models.LdaModel(corpus=tfidf_corpus, id2word=dictionary, num_topics=100)  # 生成lda model
    # 生成corpus of lsi
    lda_corpus = [lda_model[tfidf_doc] for tfidf_doc in tfidf_corpus]  # 转换成lda向量

    # 生成随机映射（Random Projections，RP, 优点：减小空维度、CPU和内存都很友好）
    rp_model = models.RpModel(tfidf_corpus, num_topics=500)
    rp_corpus = [rp_model[tfidf_doc] for tfidf_doc in tfidf_corpus]  # 转换成随机映射tfidf向量

    # 分层狄利克雷过程（Hierarchical Dirichlet Process，HDP ,一种无参数贝叶斯方法）
    hdp_model = models.HdpModel(doc_bow_corpus, id2word=dictionary)
    hdp_corpus = [hdp_model[doc_bow] for doc_bow in doc_bow_corpus]  # 转换成HDP向量

    # 文档向量和词向量 (Doc2Vec and Word2Vec)
    tld_list = []
    for ind, line_list in enumerate(corpus):
        tld_list.append(TaggedDocument(line_list, tags=[str(ind)]))
    d2v_model = Doc2Vec(tld_list, min_count=5, window=3, size=100, sample=1e-3, negative=5,iter=15)
    # 由于Doc2vec的训练过程也可以同时训练Word2vec，所以可以直接获取两个模型，全部保存起来：
    # model.save(save_model_d2v_file_path)
    # model.save_word2vec_format(save_model_w2v_file_path, binary=True)

    # 将文本转换成向量矩阵
    docvecs = d2v_model.docvecs
    docvecs_matrix = np.asarray(docvecs)
    # print(docvecs_matrix.shape)

'''-----------5. 自定义规则提取特征词----------------'''

import jieba.posseg as ps

# 针对不同业务场景（评论情感判断），可以自定义特征抽取规则（完全freestyle，不一定非得用算法来提取，只要有效果就ok）
def extract_feature_words():
    text = '成都的美食真的太多了，美味又便宜，简直就是吃货的天堂啊！'
    user_pos_list = ['a', 'ad', 'an', 'n']  # 用户自定义特征词性列表
    for word, pos in ps.cut(text):
        if pos in user_pos_list:
            print(word, pos)

if __name__ == '__main__':
    # sklearn_tfidf_feature()
    # gensim_feature()
    extract_feature_words()


