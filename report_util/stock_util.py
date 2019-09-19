#!/usr/bin/python
# coding=utf8
import datetime
import io

import pyquery
import pandas as pd

import requests

__author__ = 'Jam'
__date__ = '2019/2/19 16:40'


def get_stock_type(stock_code):
    assert type(stock_code) is str, "stock code need str type"
    if stock_code.startswith(("sh", "sz")):
        return stock_code[:2]
    if stock_code.startswith(
            ("50", "51", "60", "90", "110", "113", "132", "204")
    ):
        return "sh"
    if stock_code.startswith(
            ("00", "13", "18", "15", "16", "18", "20", "30", "39", "115", "1318")
    ):
        return "sz"
    if stock_code.startswith(("5", "6", "9", "7")):
        return "sh"
    return "sz"


def get_code_type(code):
    if code.startswith(("00", "30", "60")):
        return "stock"
    return "fund"


def round_price_by_code(price, code):
    if isinstance(price, str):
        return price

    typ = get_code_type(code)
    if typ == "fund":
        return "{:.3f}".format(price)
    return "{:.2f}".format(price)


def get_ipo_info(only_today=False):
    response = requests.get(
        "http://vip.stock.finance.sina.com.cn/corp/go.php/vRPD_NewStockIssue/page/1.phtml",
        headers={"accept-encoding": "gzip, deflate, sdch"},
    )
    html = response.content.decode("gbk")

    html_obj = pyquery.PyQuery(html)
    table_html = html_obj("#con02-0").html()

    df = pd.read_html(
        io.StringIO(table_html),
        skiprows=3,
        converters={"证券代码": str, "申购代码": str},
    )[0]
    if only_today:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        df = df[df["上网发行日期↓"] == today]
    return df
