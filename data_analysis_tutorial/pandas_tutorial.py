#!/usr/bin/python
# coding=utf8
import re

from report_util.data_analysis_head import *


def pandas_tutorial():
    print pd.__version__
    pd.show_versions()
    data = {'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat', 'dog', 'dog'],
            'age': [2.5, 3, 0.5, np.nan, 5, 2, 4.5, np.nan, 7, 3],
            'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
            'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}

    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    df = pd.DataFrame(data, index=labels)
    print df.info()
    print df.describe()
    print df.iloc[:3]
    print df.head(3)
    print df.loc[:, ['animal', 'age']]
    print df[['animal', 'age']]
    print df.loc[df.index[[3, 4, 8]], ['animal', 'age']]
    print df[df['visits'] > 3]
    print df[df['age'].isnull()]
    print df[(df['animal'] == 'cat') & (df['age'] < 3)]
    print df[df['age'].between(2, 4)]
    df.loc['f', 'age'] = 1.5
    print df
    print  df['visits'].sum()
    df = df.drop('k')
    print df
    print df['animal'].value_counts()
    print df.sort_values(by=['age', 'visits'], ascending=[False, True])
    df['priority'] = df['priority'].map({'yes': True, 'no': False})
    df['animal'] = df['animal'].replace('snake', 'python')
    print df.loc[df['A'].shift() != df['A']]
    print  df.drop_duplicates(subset='A')


def data_clean():
    df = pd.DataFrame({'From_To': ['LoNDon_paris', 'MAdrid_miLAN', 'londON_StockhOlm',
                                   'Budapest_PaRis', 'Brussels_londOn'],
                       'FlightNumber': [10045, np.nan, 10065, np.nan, 10085],
                       'RecentDelays': [[23, 47], [], [24, 43, 87], [13], [67, 32]],
                       'Airline': ['KLM(!)', '<Air France> (12)', '(British Airways. )',
                                   '12. Air France', '"Swiss Air"'],
                       'task_ids': ['1,2,3,4', '4,5,6,7', '1,2,3,8', '9', '10']})

    print df
    df['FlightNumber'] = df['FlightNumber'].interpolate().astype(int)
    print df
    temp = df.From_To.str.split('_', expand=True)
    print temp
    temp.columns = ['From', 'To']
    temp['From'] = map(lambda x: x.capitalize(), temp['From'])
    temp['To'] = temp['To'].str.capitalize()
    print temp

    df = df.drop('From_To', axis=1)
    df = df.join(temp)
    df['Airline'] = df['Airline'].str.extract('([a-zA-Z\s]+)', expand=False).str.strip()
    delays = df['RecentDelays'].apply(pd.Series)
    print  df['RecentDelays']
    print  delays
    delays.columns = ['delay_{}'.format(n) for n in range(1, len(delays.columns) + 1)]
    df = df.drop('RecentDelays', axis=1).join(delays)
    print df
    print df['delay_1'].shift(1).corr(df['delay_1'])

    df.sort_values(by=['Airline', 'FlightNumber'], ascending=[True, False], inplace=True)
    taskids = df['task_ids'].str.cat(sep=',')

    df['cat'] = df['task_ids'].str.cat(df['Airline'], sep='_')
    df[['split_1', 'split_2']] = df['cat'].str.split('_', expand=True)
    df['fanadd_ratio'] = df['fanadd'] / df['3']
    df['fanadd_ratio'] = df['fanadd_ratio'].replace([np.inf, -np.inf], np.nan).fillna(0)

    print df
    print taskids


def mutiindex_use():
    letters = ['A', 'B', 'C']
    numbers = list(range(10))

    mi = pd.MultiIndex.from_product([letters, numbers])
    s = pd.Series(range(30), index=mi)
    print s

    print s.index.is_lexsorted()

    print s.loc[:, [1, 3, 6]]
    print s.loc[pd.IndexSlice[:'B', 5:]]
    print s.sum(level=0)
    print s.unstack().sum(axis=0)

    new_s = s.swaplevel(0, 1)
    print new_s, type(new_s)
    print new_s.index.is_lexsorted()
    new_s = new_s.sort_index()
    print new_s

    mi = pd.MultiIndex.from_product([letters, numbers])
    s = pd.Series(range(30), index=mi)
    print s

    ## 多层index合并为一层
    s.index = ['%s%s' % (a, b) for a, b in s.index]
    print s


def category_use():
    c = pd.Categorical([2, 1, 1, 3], ordered=True)
    print c
    s = pd.Series([2, 1, 1, 3])
    s = s.astype('category')
    print s
    c = pd.Categorical([1, 2, 3, 4, 5, 6, 7], categories=[3, 2, 1, 4, 5, 6, 7], ordered=True).sort_values()

    print c
    print  c.T


def cut_use():
    cut1 = pd.cut(np.array([1, 7, 5, 4, 6, 3]), 3, retbins=True)
    print  cut1

    cut2 = pd.cut(np.array([1, 7, 5, 4, 6, 3]), 3, labels=["bad", "medium", "good"])
    print cut2

    cut3 = pd.cut([0, 1, 1, 2], 4, labels=False)
    print  cut3

    list_cut = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cut4 = pd.cut(list_cut, bins=[min(list_cut) - 1, 2, 9, max(list_cut) + 1],
                  labels=[u'2以下包含2', u'2<x<=9', u'9以上不包含9'])
    print cut4

    prices = np.array([12, 20, 28])
    times = np.arange(24)
    bins = np.digitize(times, bins=[7, 17, 24])

    print prices
    print times
    print bins
    print prices[bins]

    cut5 = pd.cut(times, bins=[-1, 7, 17, 24], labels=prices)
    print cut5

    pass


def corr_use():
    df = pd.DataFrame({'A': np.random.randint(1, 100, 10),
                       'B': np.random.randint(1, 100, 10),
                       'C': np.random.randint(1, 100, 10)})

    print df.corr()
    print df['A'].corr(df['B'])
    print df['B'].corr(df['A'])
    print df['A'].corr(df['C'])
    print df['B'].corr(df['C'])
    pass


def rolling_test():
    pd.options.display.float_format = '{:,.4f}'.format
    df = pd.DataFrame(
        np.random.randn(10, 4),
        index=pd.date_range('1/1/2000', periods=10),
        columns=['A', 'B', 'C', 'D']
    )

    ## 数据错1行，向前或者向后
    df['A_next_value'] = df['A'].shift(1)
    df.loc[df.index[0], 'A_next_value'] = 0
    df['A_last_value'] = df['A'].shift(-1)
    df.loc[df.index[-1], 'A_last_value'] = 0
    df['A_sum'] = df['A'].cumsum()
    print df

    ## 5各单位移动求和
    df['A_moving_sum5'] = df['A'].rolling(window=5, min_periods=1).aggregate(np.sum)
    print df

    ## 5各单位移动求平均
    df['A_moving_mean5'] = df['A'].rolling(window=5, min_periods=1).aggregate(np.mean)
    print df

    ## dict merge
    x = {'a': 1, 'b': 2}
    y = {'b': 3, 'c': 4}
    z = {'d': 5, 'e': 6, 'b': 100}
    print dict(x, **y)
    y.update(z)
    print y


def read_html_test():
    tbl = u"""
    <table cellpadding="0" cellspacing="0" border="0" class="qikanmore-result">
        <tbody><tr>
          <th><div style="width:27px">&nbsp;</div></th>
          <th width="72%">报告标题</th>
          <th width="10%">类型</th>
          <th width="14%" align="center">分享时间</th>
        </tr>
            <tr>
              <td>
                <img src="/newweb/res/img/file/pdf.gif">
              </td>
              <td class="td2"><a href="/docdetail_2497560.html" target="_blank" title="东方证券-传媒行业CTR三季度数据总结：广告行业下滑明显，电梯媒体影响较小-181125">东方证券-传媒行业CTR三季度数据总结：广告行业下滑明显，电梯媒体影响...</a></td>
              <td>季刊</td>
              <td>2018-11-26</td>
            </tr>
            <tr>
              <td>
                <img src="/newweb/res/img/file/pdf.gif">
              </td>
              <td class="td2"><a href="/docdetail_2497464.html" target="_blank" title="艾媒咨询-2018Q3中国在线直播行业季度监测报告-181126">艾媒咨询-2018Q3中国在线直播行业季度监测报告-181126</a></td>
              <td>季刊</td>
              <td>2018-11-26</td>
            </tr>
            <tr>
              <td>
                <img src="/newweb/res/img/file/pdf.gif">
              </td>
              <td class="td2"><a href="/docdetail_2497290.html" target="_blank" title="天风证券-建筑装饰行业2018年三季度基金持仓报告：基建获增仓，园林、装饰减仓；政策改善下行业配置吸引力增加-181126">天风证券-建筑装饰行业2018年三季度基金持仓报告：基建获增仓，园林、...</a></td>
              <td>季刊</td>
              <td>2018-11-26</td>
            </tr>
        </tbody>
      </table>
    """
    url_base = 'http://www.hibor.com.cn'

    ## read_html 只能识别<td>标签内部的文本txt数据,如果要提取href 需要把href从<a>标签中通过正则表达式提取出来，不然标签内部的有用的数据将无法获取
    tbl = re.sub(r'<a.*?href="(.*?)".*?title="(.*?)">.*?</a>', '{}\\1 & \\2'.format(url_base), tbl)
    print tbl

    df = pd.read_html(tbl)[0]

    df = df.iloc[1:, 1:]
    df.columns = ['content', 'type', 'date']

    ## expand=True  将list 分列
    df['url title'.split()] = df['content'].str.split('&', expand=True)
    df['title'] = df['title'].apply(lambda xx: xx.replace(',', '，').rsplit('-', 1)[0])

    print df.columns
    print df['date type url title'.split()]


def get_percent(num):
    percent_num = "{0:.2f}%.".format(100 * num)
    print  percent_num, type(percent_num)


def get_dataframe_rank():
    data = {'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat', 'dog', 'dog'],
            'age': [2.5, 3, 0, 9, 5, 2, 4.5, 9, 7, 3],
            'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
            'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}

    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    df = pd.DataFrame(data, index=labels)
    df = df.drop_duplicates(subset=['stock_id', 'year'], keep='first')
    df['age_rank'] = df['age'].rank(method='average', pct=True)
    print ord('A')

    print int((1 - 0.1) * 8)
    print chr(int((1 - 0.1) * 8) + ord('A'))
    # df['age_chr'] =  df['age_rank'].apply(lambda xx: chr((int((1 - xx) * 8)) + ord('A')) if not np.isnan(xx) else np.nan)
    df['age_rank_chr'] = df['age_rank'].apply(
        lambda xx: chr((int((1 - xx) * 8)) + ord('A')) if not np.isnan(xx) else np.nan)
    print df['age age_rank age_rank_chr'.split()]


def dataframe_group_concact():
    data = {'product_id': [23, 65, 66, 98, 998, 798],
            'category': ['cat1', 'cat2', 'cat1', 'cat1', 'cat1', 'cat2'],
            'number_of_purchase': [18, 19, 4, 9, 1, 8]}

    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=df.columns.tolist(), keep='first')
    df = df.sort_values(by='number_of_purchase', ascending=False)
    print df
    print df.where(df['product_id'] > 100).dropna(subset=['product_id'])

    df = df['category product_id number_of_purchase'.split()].groupby('category').agg(lambda xx: list(xx))
    print df
    df['number_of_purchase'] = df['number_of_purchase'].apply(lambda x: '&'.join([str(elem) for elem in x]))
    df['product_id'] = df['product_id'].apply(lambda x: '&'.join([str(elem) for elem in x]))

    # df_group = df.unstack(0)
    # print df_group
    # df_group = df_group.reset_index()
    # print df_group
    # df_group.columns = ['%s%s' % (lev1, '_%s' % lev2 if lev2 else '') for lev1, lev2 in df_group.columns


if __name__ == "__main__":
    # pandas_tutorial()
    # data_clean()
    # mutiindex_use()
    # cut_use()
    # category_use()
    # corr_use()
    # rolling_test()
    # read_html_test()
    # get_percent(1.1222)
    # get_dataframe_rank()
    dataframe_group_concact()
