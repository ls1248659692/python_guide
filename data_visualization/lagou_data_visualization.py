# coding:utf-8
# !/usr/bin/env python
import json
import os
import re
import time
import pickle
import traceback
from multiprocessing import Pool
from compiler.ast import flatten

import jieba
import requests

from pyecharts import Geo

from scipy.misc import imread

from wordcloud import WordCloud

from  report_util.data_analysis_head import *
from constant import LagouDataVisualization as LAGOU

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filedir = os.path.join(PROJECT_ROOT, LAGOU.FILE_DOWNLOAD_PATH)
filepath = os.path.join(filedir, 'lagou_data_visualization.csv')


def save_cookies():
    response = requests.get(
        LAGOU.COOKIES_URL, headers=LAGOU.COOKIES_HEADER, timeout=10
    )

    if response.status_code == 200:
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
        with open('cookies', 'w') as f:
            pickle.dump(cookies_dict, f)
        return response.cookies
    else:
        print LAGOU.ERROR_MSG.format(status_code=response.status_code)


def get_cookies():
    with open('cookies', 'r') as f:
        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))

    return cookies


def get_job_max_pageno(needAddtionalResult='false', keyword='python'):
    form = {
        'first': 'true',
        'kd': keyword,
        'pn': '1'
    }

    response = requests.post(
        LAGOU.JOB_URL.format(need=needAddtionalResult),
        data=form,
        headers=LAGOU.Job_HEADER,
        # cookies=save_cookies(),
        timeout=5
    )

    if response.status_code == 200:
        try:
            total_count = json.loads(response.text)['content']['positionResult']['totalCount']
            max_page_no = int(int(total_count) / 15)
            print LAGOU.MAX_PAGENO.format(keyword=keyword, max_page_no=max_page_no, total_count=total_count)
            return max_page_no
        except:
            traceback.print_exc()
            return False
    else:
        print LAGOU.ERROR_MSG.format(status_code=response.status_code)


def spider_lagou_job_data(page_num, needAddtionalResult='false', keyword='python'):
    form = {
        'first': 'true',
        'kd': keyword,
        'pn': str(page_num)
    }

    response = requests.post(
        LAGOU.JOB_URL.format(need=needAddtionalResult),
        data=form,
        headers=LAGOU.Job_HEADER,
        # cookies=save_cookies(),
        timeout=5
    )

    if response.status_code == 200:
        try:
            data_list = json.loads(response.text)['content']['positionResult']['result']
            with open(os.path.join(filedir, 'lagou_job_data.txt'), "a+") as f:
                for data in data_list:
                    f.writelines('%s\n' % data)
            print LAGOU.OK_MSG.format(n=page_num)
        except:
            traceback.print_exc()
    else:
        print LAGOU.ERROR_MSG.format(status_code=response.status_code)

    time.sleep(LAGOU.WAIT_TIME)


def multiprocess_spider_job_data(needAddtionalResult='false', keyword='python'):
    max_page_no = get_job_max_pageno(needAddtionalResult, keyword)

    print('multiprocess spider start.')
    pool = Pool(processes=5)
    pool.map(spider_lagou_job_data, range(1, max_page_no))
    pool.close()
    pool.join()
    print('multiprocess spider end.')


def save_job_data():
    with open(os.path.join(filedir, 'lagou_job_data.txt'), 'r') as f:
        data_list = f.readlines()

    dict_list = []
    for data in data_list:
        try:
            data = eval(data.strip())
            dict_list.append(data)
        except:
            continue

    df = pd.DataFrame(dict_list)
    show_cols = ['companyId', 'companyFullName', 'companyShortName', 'companyLabelList',
                 'city', 'companySize', 'education', 'financeStage', 'businessZones', 'salary',
                 'firstType', 'secondType', 'thirdType', 'skillLables', 'stationname', 'workYear']
    dataset = df[show_cols].fillna('')

    cols_join = 'companyLabelList businessZones skillLables'.split()
    cols_replace = 'firstType secondType thirdType'.split()
    dataset['companyId'] = dataset['companyId'].apply(lambda xx: int(float(xx)) if xx else 0)
    dataset[cols_join] = dataset[cols_join].applymap(lambda xx: ','.join(xx) if xx  else  '')
    dataset[cols_replace] = dataset[cols_replace].applymap(lambda xx: xx.replace('|', ',') if xx  else  '')

    print dataset.head()
    print dataset.tail()
    dataset.to_csv(filepath, encoding='utf-8', index=False)


def spider_lagou_company(havemark=0):
    ## havemark: 0 for not showing interviewees' remark;
    #            1 for showing interviewees' remark;

    COMPANY_LIST = list()

    for n in range(20):
        form = {
            'first': 'false',
            'pn': str(n),
            'sortField': '0',
            'havemark': str(havemark)
        }

        response = requests.post(
            LAGOU.COMPANY_URL.format(havemark=havemark),
            data=form,
            headers=LAGOU.COMPANY_HEADER,
            # cookies=save_cookies(),
            timeout=5
        )

        if response.status_code == 200:
            try:
                company_list_per_page = response.json()['result']
                for company in company_list_per_page:
                    COMPANY_LIST.append([company['companyId'], company['companyShortName'],
                                         company['city'], company['companyFeatures'],
                                         company['companyFullName'], company['financeStage'], company['industryField'],
                                         company['interviewRemarkNum'], company['positionNum'], company['processRate']])

                print LAGOU.OK_MSG.format(n=n + 1)
            except:
                traceback.print_exc()
        else:
            print LAGOU.ERROR_MSG.format(status_code=response.status_code)

        time.sleep(LAGOU.WAIT_TIME)

    cols_to_show = ['companyId', 'companyShortName', 'city', 'companyFeatures', 'companyFullName',
                    'financeStage', 'industryField', 'interviewRemarkNum', 'positionNum', 'processRate']
    dataset = pd.DataFrame(COMPANY_LIST, columns=cols_to_show)
    dataset.to_csv(os.path.join(filedir, 'lagou_company.csv'), encoding='gbk', index=False)


def data_visualization():
    data = pd.read_csv(filepath, encoding='utf-8')
    data['salary'] = data['salary'].apply(lambda xx: str(xx).split('-')[0])

    edu_dataset = data['education'].value_counts()
    wrk_dataset = data['workYear'].value_counts()
    cpy_dataset = data['companySize'].value_counts()
    salary_dataset = data['salary'].value_counts()[:10]

    plot_bar_chart(
        edu_dataset,
        [u"不限", u"大专", u"本科", u"硕士"],
        u'教育背景需求分析',
        u"教育背景",
        u"数量/个"
    )

    plot_bar_chart(
        wrk_dataset,
        [u"不限", u"应届毕业生", u"1年以下", u"1-3年", u"3-5年", u"5-10年"],
        u'工作年限需求分析',
        u"工作年限",
        u"数量/个"
    )

    plot_bar_chart(
        cpy_dataset,
        [u"少于15人", u"15-50人", u"50-150人", u"150-500人", u"500-2000人", u"2000人以上"],
        u'公司体量需求分析',
        u"公司体量",
        u"数量/个"
    )

    plot_bar_chart(
        salary_dataset,
        [u"5k", u"6k", u"8k", u"10k", u"12k", u"15k", u"18k", u"20k", u"25k", u"30k"],
        u'薪资水平需求分析',
        u"薪资水平",
        u"数量/个"
    )


def plot_bar_chart(dataset, order, title, xlable, ylable):
    fig, ax = plt.subplots(figsize=(14, 10))

    sns.barplot(x=dataset.index, y=dataset.values, palette="deep", order=order)
    ax.set_title(title, fontsize=18, position=(0.5, 1.05))
    ax.set_xlabel(xlable, fontsize=12)
    ax.set_ylabel(ylable, fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=-45)

    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        plt.annotate(
            y_value,
            (x_value, y_value),
            xytext=(0, 5) if y_value > 0  else (0, -5),
            textcoords="offset points",
            ha='center',
            va='bottom' if y_value > 0  else 'top'
        )

    plt.savefig(filedir + u'{}.png'.format(title), dpi=80, bbox_inches='tight')


def word_segmentation():
    data = pd.read_csv(filepath, encoding='utf-8').fillna('')
    image = imread(os.path.join(PROJECT_ROOT, LAGOU.BACKGROUND))

    df = pd.read_csv(
        os.path.join(PROJECT_ROOT, LAGOU.STOPWORDS),
        encoding='utf8',
        index_col=False
    )

    jieba.load_userdict(os.path.join(PROJECT_ROOT, LAGOU.USERDICT))  ## 添加多个词汇
    stopwords = list(df['stopword'].unique())
    stopwords.extend([u'技术', u'高端', u'职位', u'企业', ',', '工程师', '类', '实施', 'IT'])  ## 添加停止词

    ## 需求岗位与技能词汇
    word_list = flatten([list(jieba.cut(row['firstType']))
                         for _, row in data.iterrows()])
    word_list.extend(flatten([list(jieba.cut(row['secondType']))
                              for _, row in data.iterrows()]))
    word_list.extend(flatten([list(jieba.cut(row['thirdType']))
                              for _, row in data.iterrows()]))

    word_list = [word for word in word_list if word not in stopwords]
    words_count = pd.value_counts(word_list).to_dict()
    print pd.value_counts(word_list)

    wordcloud = WordCloud(
        background_color="white",
        mask=image,
        font_path=LAGOU.TTF,
        max_words=5000,
        scale=1.5
    )

    wordcloud = wordcloud.fit_words(words_count)

    plt.figure(
        figsize=(10, 6),
        dpi=100
    )

    plt.axis("off")
    wordcloud.to_file(filedir + 'data_wordcloud.png')
    plt.imshow(wordcloud)
    plt.show()
    plt.close()


def geographical_location_distribution():
    data = pd.read_csv(filepath, encoding='gbk')
    data['salary'] = data['salary'].apply(lambda xx: re.sub(u'k|K|以上', '', xx))
    data['min_salary'] = data['salary'].apply(lambda xx: float(xx.split('-')[0]) * 1000)
    data['max_salary'] = data['salary'].apply(
        lambda xx: float(xx.split('-')[1]) * 1000 if len(xx.split('-')) > 1 else float(xx) * 1000)
    # print  data[data['min_salary'] == data['max_salary']]  ##  xx以上
    dataset = [(city, min_salary) for city, min_salary in data['city min_salary'.split()].values]

    geo = Geo("Python Job Distribution", "", title_pos="center", width=2000, height=1200, background_color='#404a59')
    attr, value = geo.cast(dataset)
    geo.add("", attr, value, type="effectScatter",
            is_visualmap=True, maptype='china', visual_range=[0, 300],
            effect_scale=5, symbol_size=5, visual_text_color="#fff")

    geo.render(filedir + 'job_distribution.html')
    # geo.render(path_sign + 'snapshot.png')


def main():
    # save_cookies()
    # get_cookies()
    # get_job_max_pageno()
    # spider_lagou_job_data()
    # multiprocess_spider_job_data()
    # save_job_data()
    # spider_lagou_company()
    data_visualization()
    # word_segmentation()
    # geographical_location_distribution()
    pass


if __name__ == "__main__":
    main()
