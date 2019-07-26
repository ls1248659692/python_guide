#!/usr/bin/python
# coding=utf8
import os
import webbrowser

import pandas_profiling
from pd2ppt import df_to_powerpoint

from  report_util.data_analysis_head import *


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filepath = os.path.join(PROJECT_ROOT, 'static/data_visualization/lagou/')
df = pd.read_csv(filepath + 'lagou_data_visualization.csv', encoding='utf-8')


def df_profiling():
    pfr = pandas_profiling.ProfileReport(df)
    pfr.to_file(filepath + "lagou_data_profile.html")
    webbrowser.open_new_tab(filepath + "lagou_data_profile.html")


def create_description_table(df, descriptions, round_num=2):
    df_desc = df.dtypes.to_frame(name='Data Type')
    df_desc['Description'] = descriptions
    df_desc['Missing Values'] = df.isnull().sum()
    df_desc['Mean'] = df.select_dtypes('number').mean().round(round_num)
    df_desc['Most Common'] = df.apply(lambda x: x.value_counts().index[0])
    df_desc['Most Common Ct'] = df.apply(lambda x: x.value_counts().iloc[0])
    df_desc['Unique Values'] = df.nunique()
    print  df_desc
    return df_desc


def statistics_summary(df, column, condiction):
    data = df[condiction]
    statistics = data[column].describe()
    print statistics, type(statistics)

    statistics['range'] = statistics['max'] - statistics['min']
    statistics['var'] = statistics['std'] / statistics['mean']
    statistics['dis'] = statistics['75%'] - statistics['25%']

    print(statistics)


def df2ppt():
    df = pd.DataFrame(
        {'District': ['Hampshire', 'Dorset', 'Wiltshire', 'Worcestershire'],
         'Population': [25000, 500000, 735298, 12653],
         'Ratio': [1.56, 7.34, 3.67, 8.23]})

    shape = df_to_powerpoint(
        r"test2.pptx", df,
        left=1, top=1, width=10, height=15,
        col_formatters=['', '.', '.3'], rounding=['', 3, ''])
    print shape


def main():
    descriptions = 'Company Id,Company Name,Company Short Name,Company Label,City,Company Size,Education'.split(',')
    descriptions += 'Finance Stage,Business Zones,Salary,First Type,Second Type,Third Type,Skill Lables,Station Name,Work Year'.split(',')
    df_profiling()
    # create_description_table(df, descriptions)
    # df2ppt()
    pass


if __name__ == '__main__':
    main()
