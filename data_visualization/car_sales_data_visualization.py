# coding:utf-8
# !/usr/bin/env python

from pyecharts import Geo, Timeline

from  report_util.data_analysis_head import *

__author__ = 'Jam'
__date__ = '2019/2/11 17:45'


def car_sales_volume_data_clean():
    data = pd.read_excel("./data/car_sales_volume_data.xlsx", sheet_name=u"myresult (3)", encoding='utf-8')
    float_cols = [year for year in range(1997, 2019)]
    not_replace = [u'池州市', u'宣城市', u'眉山市', u'达州市', u'庆阳市', u'广安市', u'贺州市', u'来宾市', u'崇左市']
    data['city'] = data['city'].fillna('').apply(lambda xx: xx.replace(u'市', '') if xx not in not_replace else xx)
    city_none = [u'黔西南布依族苗族自治州', u'乌兰察布']
    data = data[~data['city'].isin(city_none)]
    data[float_cols] = data[float_cols].fillna(0).applymap(lambda xx: int(xx) if xx else 0)
    cols_show = ['city'] + float_cols
    data = data[cols_show]
    df_group = data.groupby('city').sum()
    df_group.to_csv("./data/car_sales_volume_data.csv")

    print df_group.columns
    print df_group.head()
    print df_group.tail()


def geographical_location_amount_distribution():
    data = pd.read_csv("./data/car_sales_volume_data.csv", encoding='utf-8')
    data = data[data['city'].str.len() > 1]

    city_none = [
        u'三沙', u'中卫', u'临沧', u'丽江',
        u'克孜勒苏柯尔克孜自治州', u'其它',
        u'固原', u'新疆自治区直辖', u'普洱',
        u'河南省省直辖', u'海南省省直辖', u'湖北省省直辖'
    ]
    data = data[~data['city'].isin(city_none)]
    int_cols = [str(col) for col in range(1998, 2019)]
    data[int_cols] = data[int_cols].applymap(lambda xx: float(xx))

    timeline = Timeline(is_auto_play=False, timeline_bottom=1250, width=2480, height=1330)
    for year in range(1998, 2019):
        dataset = [(city, sales) for city, sales in data[('city %s' % year).split()].values]
        print dataset

        geo = Geo(
            "%s - Car Sales Num Amount Distribution" % year,
            "",
            title_pos="center",
            title_color="black",
            width=2700,
            height=1340,
            background_color='#ffffff'
        )
        attr, value = geo.cast(dataset)
        geo.add(
            "",
            attr,
            value,
            maptype='china',
            visual_range=[0, 300000],
            visual_text_color="black",
            type="heatmap",
            is_visualmap=True,
            effect_scale=5,
            symbol_size=5,
        )
        timeline.add(geo, year)

    timeline.render('./car_sales_visualization/car_sales_num_amount.html')


def geographical_location_ratio_distribution():
    data = pd.read_csv("./data/car_sales_volume_data.csv", encoding='utf-8')
    data = data[data['city'].str.len() > 1]

    data = calc_ratio_percent(data)
    data[range(1998, 2019)] = data[range(1998, 2019)].applymap(lambda xx: round(xx * 100, 4))
    cols_show = ['city'] + range(1998, 2019)
    data = data[cols_show]

    city_none = [
        u'三沙', u'中卫', u'临沧', u'丽江',
        u'克孜勒苏柯尔克孜自治州', u'其它',
        u'固原', u'新疆自治区直辖', u'普洱',
        u'河南省省直辖', u'海南省省直辖', u'湖北省省直辖'
    ]
    data = data[~data['city'].isin(city_none)]
    data.to_excel('./car_sales_visualization/car_sales_num_ratio.xlsx')

    timeline = Timeline(is_auto_play=False, timeline_bottom=1250, width=2480, height=1330)
    for year in range(1998, 2019):
        dataset = [(city, sales) for city, sales in data[['city'] + [year]].values]

        geo = Geo(
            "%s - Car Sales Num Ratio Distribution" % year,
            "",
            title_pos="center",
            title_color="black",
            width=2480,
            height=1330,
            background_color='#ffffff'
        )
        attr, value = geo.cast(dataset)
        geo.add(
            "",
            attr,
            value,
            type="effectScatter",
            is_visualmap=True,
            maptype='china',
            visual_range=[-100, 100],
            visual_text_color="black",
            effect_scale=5,
            symbol_size=5
        )

        timeline.add(geo, year)

    timeline.render('./car_sales_visualization/car_sales_num_ratio.html')


def calc_ratio_percent(df):
    for year in range(1998, 2019):
        year_str, last_year_str = str(year), str(year - 1)

        year_ratio = []
        for el1, el2 in df[[last_year_str, year_str]].values:
            if el1 > 0:
                ratio = (float(el2) - float(el1)) / float(el1)
                if -1 <= ratio <= 1:
                    year_ratio.append(ratio)
                elif ratio < -1:
                    year_ratio.append(-1.0)
                elif ratio > 1:
                    year_ratio.append(1.0)

            elif el1 == 0 and el2 == 0:
                year_ratio.append(0)
            elif el1 == 0 and el2 > 0:
                year_ratio.append(1.0)

        df[year] = year_ratio

    return df


def geographical_location_GDP_amount_distribution():
    data = pd.read_excel("./data/car_sales_data.xlsx", sheet_name=u"人均GDP", encoding='utf-8')
    data.columns = [str(col).split('-')[0] for col in data.columns]

    float_cols = [str(year) for year in range(1998, 2018)]
    not_replace = [
        u'池州市', u'宣城市', u'眉山市', u'达州市', u'庆阳市',
        u'广安市', u'贺州市', u'来宾市', u'崇左市', u'临沧市',
        u'固原市', u'中卫市', u'丽江市'
    ]
    data['city_name'] = data['city_name'].apply(lambda xx: xx.replace(u'市', '') if xx not in not_replace else xx)
    city_none = [u'黔西南布依族苗族自治州', u'乌兰察布', u'巴音郭楞蒙古自治州（库尔勒）']
    data = data[~data['city_name'].isin(city_none)]
    data[float_cols] = data[float_cols].fillna(0).applymap(lambda xx: round(xx, 2) if xx else 0)
    cols_show = ['city_name'] + float_cols
    data = data[cols_show]

    max_range = data['2017'].max()
    timeline = Timeline(is_auto_play=False, timeline_bottom=1250, width=2480, height=1330)
    for year in float_cols:
        dataset = [(city, sales) for city, sales in data[('city_name %s' % year).split()].values]

        geo = Geo(
            "%s - GDP Amount Distribution" % year,
            "",
            title_pos="center",
            title_color="black",
            width=2700,
            height=1340,
            background_color='#ffffff'
        )
        attr, value = geo.cast(dataset)
        geo.add(
            "",
            attr,
            value,
            maptype='china',
            visual_range=[0, max_range],
            visual_text_color="black",
            type="heatmap",
            is_visualmap=True,
            effect_scale=5,
            symbol_size=5,
        )
        timeline.add(geo, year)

    timeline.render('./car_sales_visualization/GDP_amount_distribution.html')


def geographical_location_GDP_ratio_distribution():
    data = pd.read_excel("./data/car_sales_data.xlsx", sheet_name=u"人均GDP", encoding='utf-8')
    data.columns = [str(col).split('-')[0] for col in data.columns]

    float_cols = [str(year) for year in range(1998, 2018)]
    not_replace = [
        u'池州市', u'宣城市', u'眉山市', u'达州市', u'庆阳市',
        u'广安市', u'贺州市', u'来宾市', u'崇左市', u'临沧市',
        u'固原市', u'中卫市', u'丽江市'
    ]
    data['city_name'] = data['city_name'].apply(lambda xx: xx.replace(u'市', '') if xx not in not_replace else xx)
    city_none = [u'黔西南布依族苗族自治州', u'乌兰察布', u'巴音郭楞蒙古自治州（库尔勒）']
    data = data[~data['city_name'].isin(city_none)]
    data[float_cols] = data[float_cols].fillna(0).applymap(lambda xx: round(xx, 2) if xx else 0)
    cols_show = ['city_name'] + float_cols
    data = data[cols_show]
    data = calc_ratio_percent(data)
    data[range(1999, 2018)] = data[range(1999, 2018)].applymap(lambda xx: round(xx * 100, 2))
    data.to_excel('./car_sales_visualization/GDP_ratio_distribution.xlsx')

    timeline = Timeline(is_auto_play=False, timeline_bottom=1250, width=2480, height=1330)

    for year in range(1999, 2018):
        dataset = [(city, sales) for city, sales in data[['city_name'] + [year]].values]

        geo = Geo(
            "%s - Car Sales Num Ratio Distribution" % year,
            "",
            title_pos="center",
            title_color="black",
            width=2480,
            height=1330,
            background_color='#ffffff'
        )
        attr, value = geo.cast(dataset)
        geo.add(
            "",
            attr,
            value,
            type="effectScatter",
            is_visualmap=True,
            maptype='china',
            visual_range=[-100.0, 100.0],
            visual_text_color="black",
            effect_scale=5,
            symbol_size=5
        )

        timeline.add(geo, year)

    timeline.render('./car_sales_visualization/GDP_ratio_distribution.html')


def main():
    # car_sales_volume_data_clean()
    # geographical_location_amount_distribution()
    geographical_location_ratio_distribution()
    # geographical_location_GDP_amount_distribution()
    # geographical_location_GDP_ratio_distribution()
    pass


if __name__ == "__main__":
    main()
