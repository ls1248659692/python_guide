# coding:utf-8
# !/usr/bin/env python

class LagouDataVisualization:
    def __init__(self):
        pass

    Cookie = 'user_trace_token=20181105095805-99f654bc-a89f-43fb-a38e-8e9300d7c24a; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166e19791202b6-0a5714015dc492-69101b7d-3686400-166e19791212b8%22%2C%22%24device_id%22%3A%22166e19791202b6-0a5714015dc492-69101b7d-3686400-166e19791212b8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LGUID=20181105095818-43df78ae-e09e-11e8-8988-525400f775ce; _ga=GA1.2.1775346865.1541383149; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAABAAAGFABEFD1CB948661C3782F164F1C504ECE9772; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543220122,1543220477,1543220490,1543228093; TG-TRACK-CODE=index_search; SEARCH_ID=6e5b6071b53a4349b601d57f3b945cd0; _gat=1; LGSID=20181126202439-3e75f08a-f176-11e8-8c02-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543235379; LGRID=20181126202938-f0f2fe5e-f176-11e8-8c02-5254005c3644'
    JOB_URL = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult={need}'
    COMPANY_URL = 'https://www.lagou.com/gongsi/0-0-0.json?havemark={havemark}'
    COOKIES_URL = 'https://m.lagou.com/'

    COOKIES_HEADER = {
        'Host': 'm.lagou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
    }

    Job_HEADER = {
        'Cookie': Cookie,
        'Origin': "https://www.lagou.com",
        'X-Anit-Forge-Code': "0",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Referer': "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
        'X-Requested-With': "XMLHttpRequest",
        'Connection': "keep-alive",
        'X-Anit-Forge-Token': "None",
        'cache-control': "no-cache",
        'Postman-Token': "c9290cbd-d3cc-403a-80b2-a4d8f1dc7024"
    }

    COMPANY_HEADER = {
        'Cookie': Cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/gongsi/0-0-0?havemark=0',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
                      'Mobile/13B143 Safari/601.1'
    }

    FILE_DOWNLOAD_PATH = "static/data_visualization/lagou/"
    BACKGROUND = "static/data_visualization/lagou/background.png"
    STOPWORDS = "static/data_visualization/stopwords_china.txt"
    TTF = "static/data_visualization/simhei.ttf"
    USERDICT = "static/data_visualization/userdict.txt"

    WAIT_TIME = 2

    MAX_PAGENO = 'the search result of {keyword}, max page no  is  {max_page_no}  and total_count is {total_count}.'
    ERROR_MSG = 'error happend status code is {status_code}.'
    OK_MSG = 'page {n} has been crawled OK.'


class GitHubData:
    def __init__(self):
        pass

    TOP25_URL = 'https://github.com/trending/{language}'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    GITHUB_HEADER = {
        'Host': "github.com",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    USERNAME = '1248659692@qq.com'
    PASSWORD = 'ls19910924!'

    ERROR_MSG = 'status code is error, status code is {}'

    EMAIL_CONFG = dict(
        smtp="smtp.sina.cn",
        email_address="18916227573m@sina.cn",
        password="asdf1234!",
        to="jaliang@capvision.com",
        title="Github Top25 Of Python",
    )

    MAIL_TEMPLATE = '''
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>Github Top25 Of Python</title>
        </head>
        <body yahoo bgcolor="#f6f8f1">
            <table align="left" bgcolor="#f6f8f1" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 425px;">
                <tr>
                    <td>
                        <table class="content" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr><th>#&nbsp;&nbsp;</th><th>title</th><th>url_link</th><th>content</th></tr>
                        {table_content}
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    '''
