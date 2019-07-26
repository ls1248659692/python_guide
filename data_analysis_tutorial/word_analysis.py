#!/usr/bin/python
# coding=utf8
import sys
import time
import traceback

import pandas as pd
import requests
from aip import AipSpeech
from bs4 import BeautifulSoup

from report_util.mysql_util import execute

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

__author__ = 'Jam'
__date__ = '2019/6/11 15:16'

APP_ID = '16483169'
API_KEY = 'dWQhEer2Q6HCp8dlLrt961As'
SECRET_KEY = 'XwFAef5c1pYeP54bkKV6EuxGWgzmL2Gi'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def word2speech(word_id, word):
    result = client.synthesis(word, 'zh', 1, {
        'vol': 8, 'per': 4
    })

    if not isinstance(result, dict):
        with open('./data/mp3/{}.mp3'.format(word_id), 'wb') as f:
            f.write(result)


def get_word():
    df = pd.read_csv('./data/word_add.csv')
    df = df['id word'.split()]

    # for word_id, word in df['id word'.split()].values:
    #     word2speech(word_id, word)

    for word_id, word in df['id word'.split()].values:
        try:
            abstract, english = get_word_comment(word)
            time.sleep(5)

            sql = '''
                            UPDATE quant.tb_english_words_quize
                            SET eng_comments = "{0}",
                                sentence = "{1}"
                            WHERE
                                id ={2};
                '''.format(english, abstract, word_id)
            execute('87', sql)
        except BaseException:
            traceback.print_exc()


def get_word_comment(word):
    url = "https://www.zdic.net/search/"

    querystring = {"sclb": "tm", "q": word}

    headers = {
        'authority': "www.zdic.net",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'referer': "https://www.zdic.net/hans/%E4%B8%9A,https://www.zdic.net/search/?sclb=tm&q=%E7%82%95",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cookie': "_ga=GA1.2.1181131621.1560240378; _gid=GA1.2.1927543198.1560240378; yewwpecookieinforecord=%2C3-8854%2C3-27%2C; yewwpcheckplkey=1560240508%2C5595a751b5aea1c1fab65f2d87ca23ba%2CEmpireCMS",
        'Cache-Control': "no-cache",
        'Postman-Token': "d8c00542-f8b4-474e-8a6c-0f540d41587e,99be2563-b603-4e71-bb98-04beb709c0e5",
        'Connection': "keep-alive",
        'cache-control': "no-cache"}

    content = BeautifulSoup(
        requests.get(
            url, headers=headers, params=querystring).content,
        'html.parser')
    try:
        abstract = content.find(
            'div', class_='content definitions jnr').find(
            'ol').text.strip().replace(u'～', word)
    except BaseException:
        abstract = ''

    try:
        english = content.find('div', class_='enbox').find(
            'p').text.strip().replace(u'英语', '').strip()
    except BaseException:
        english = ''

    print word, abstract, english
    return abstract, english


def main():
    get_word()
    # get_word_comment("炕")


if __name__ == '__main__':
    main()
