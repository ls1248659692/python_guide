#!/usr/bin/python
# coding=utf8
import os
from compiler.ast import flatten

import jieba
import nltk
from scipy.misc import imread
from wordcloud import WordCloud

from report_util.data_analysis_head import *
from report_util.mysql_util import read_sql

__author__ = 'Jam'
__date__ = '2019/3/4 15:15'

dict_file = './data/dict.txt'
user_dict_file = './data/user_dict.txt'
stopword_file = './data/stopwords.txt'
blackwords_file = './data/blackwords.txt'
blackground_pic = './data/background.png'


def get_report_title():
    select_sql = '''
                SELECT title
                FROM  quant.tb_uqer_stock_reports
                WHERE type = 'INDUSTRY'
                    AND industry RLIKE '医药'
    '''

    df = read_sql('87', select_sql)
    return df


def get_word_set(words_file):
    words_set = set()
    with open(words_file, 'r') as fp:
        for line in fp.readlines():
            word = line.strip().decode("utf-8")
            if len(word) > 0 and word not in words_set:
                words_set.add(word)
    return words_set


def select_topk(words_dict, topk=20):
    user_dict_set = get_word_set(user_dict_file)

    if not words_dict:
        return []
    else:
        words_tuple_list = sorted(words_dict.items(), key=lambda dict: dict[1], reverse=True)
        sorted_words = list(zip(*words_tuple_list)[0])

        new_sorted_words = filter(lambda key: key in user_dict_set, sorted_words)
        tags = new_sorted_words[:topk]

        return tags


def word_segmentation(text, lag):
    if lag == "eng":
        word_list = nltk.word_tokenize(text)
    elif lag == "chs":
        word_cut = jieba.cut(text, cut_all=False)
        word_list = list(word_cut)
    else:
        word_list = []
    return word_list


def words_feature_weight(words_list):
    tags_dict = {}
    user_dict_set = get_word_set(user_dict_file)

    for word in words_list:
        if tags_dict.has_key(word) and word in user_dict_set:
            tags_dict[word] += 1
        elif not tags_dict.has_key(word) and word in user_dict_set:
            tags_dict[word] = 1
        else:
            pass

    for key in tags_dict:
        tags_dict[key] = round(tags_dict[key] / len(words_list), 3)

    return ','.join(select_topk(tags_dict))


def plot_wordcloud(words_count):
    image = imread(blackground_pic)

    wordcloud = WordCloud(
        background_color="white",
        mask=image,
        font_path='./data/simhei.ttf',
        max_words=5000,
        scale=1.5
    )

    wordcloud = wordcloud.fit_words(words_count)

    plt.figure(
        figsize=(10, 6),
        dpi=100
    )

    plt.axis("off")
    wordcloud.to_file('./data/wordcloud.png')
    plt.imshow(wordcloud)
    # plt.show()
    plt.close()


def report_analysis():
    data = get_report_title()
    # print data.info()

    if os.path.exists(dict_file):
        jieba.set_dictionary(dict_file)

    if os.path.exists(user_dict_file):
        jieba.load_userdict(user_dict_file)

    stopwords_set = get_word_set(stopword_file)
    blackwords_set = get_word_set(blackwords_file)

    words_feature = flatten([word_segmentation(row['title'], 'chs')
                             for _, row in data.iterrows()])

    words_feature = [word for word in words_feature
                     if word not in (stopwords_set | blackwords_set | set(' '))]

    words_count_frequency = pd.value_counts(words_feature).to_dict()
    # plot_wordcloud(words_count_frequency)

    print pd.value_counts(words_feature)[:100]

    # data['title_feature'] = data['title'].apply(lambda xx: word_segmentation(xx, 'chs'))
    # data['tags'] = data['title_feature'].apply(lambda xx: words_feature_weight(xx))
    # data = data[data['tags'].str.len() > 1]
    #
    # print  data['title tags'.split()]


def main():
    report_analysis()


if __name__ == '__main__':
    main()
