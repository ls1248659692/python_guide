#!/usr/bin/python
# coding=utf8
import re

import requests
from lxml import etree

__author__ = 'Jam'
__date__ = '2018/12/25 15:24'


class JDong(object):
    def __init__(self):
        pass

    def get(self, url):
        try:
            r = requests.get(url)
            if r.ok:
                encoding = requests.utils.get_encodings_from_content(r.text)
                r.encoding = encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)
                return r.text
            else:
                print r.status_code
        except requests.RequestException as e:
            print e

    def search(self, keyword, page=1):
        url = 'https://search.jd.com/Search?keyword={}&enc=utf-8&page={}'.format(keyword, page)
        r = self.get(url)
        html = etree.HTML(r)
        goodslist = html.xpath('//*[@id="J_goodsList"]/ul/li')
        relist = []
        for goods in goodslist:
            link = goods.xpath('div/div[1]/a/@href')
            img = goods.xpath('div/div[1]/a/img/@src')
            price_type = goods.xpath('div/div[3]/strong/em/text()')
            price_data = goods.xpath('div/div[3]/strong/i/text()')
            name = goods.xpath('div/div[4]/a/@title')
            comment = goods.xpath('div/div[5]/strong/a/text()')
            uid = re.findall('jd.com/(.*?).html', link[0]) if link else None

            if uid:
                uid = uid[0]
                link = 'http:{}'.format(link[0]) if link else ''
                img = 'http:{}'.format(img[0]) if img else ''
                price_type = price_type[0] if price_type else ''
                price_data = price_data[0] if price_data else ''
                name = name[0] if name else ''
                comment = comment[0] if comment else ''
                relist.append({
                    'uid': uid,
                    'link': link,
                    'img': img,
                    'price_type': price_type,
                    'price_data': price_data,
                    'name': name,
                    'comment': comment
                })
        return relist

    def comment(self, product_id, page=1):
        url = 'https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=3&' \
              'page={}&pageSize=10&callback=fetchJSON_comment98vv157'.format(product_id, page)
        text = self.get(url)
        text = text.replace('javascript:void(0);', '')
        data = re.findall('fetchJSON_comment98vv157\((.*?)\}\);', text)
        if data:
            try:
                data = data[0] + '}'
                data = data.replace(' ', '')
                data = data.replace('":null', '":"null"')
                data = data.replace('":false', '":"false"')
                data = data.replace('":true', '":"true"')
                data = eval(data)
                return data
            except Exception as e:
                print('发生错误在[JDong.comment]时:{}\n请将报错内容提交到github:评论text{}'.format(e, text))
                exit()
        else:
            return {}

    def get_comment_page(self, product_id):
        data = self.comment(product_id)
        return data['maxPage'] if data else 0

    def get_color_size(self, product_id):
        url = 'https://item.jd.com/{}.html'.format(product_id)
        text = self.get(url)
        text = text.replace(' ', '')
        if 'colorSize:{}' in text or 'colorSize' not in text:
            return []
        try:
            color_size = re.findall('colorSize(.*?)}],', text)[0]
            color_size = color_size + '}]'
            color_size = re.findall('\[(.*?)\]', color_size)[0]
            color_size = '[' + color_size + ']'
            return eval(color_size)
        except Exception as e:
            print('发生错误在[JDong.get_color_size]时:{}\n请将报错内容提交到github:商品id{}'.format(e, product_id))
            exit()

    def get_skuids(self, product_id):
        color_size = self.get_color_size(product_id)
        skuids = []
        for i in color_size:
            try:
                skuids.append(str(i['SkuId']))
            except Exception as e:
                print  e
                pass
        return skuids
