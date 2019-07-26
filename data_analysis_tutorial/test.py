#!/usr/bin/python
# coding=utf8
import hashlib
import itertools
import json
import math
import os
import poplib
import random
import time
import uuid
import winsound
from collections import namedtuple
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from urlparse import urlparse, parse_qs

import html2text
import pandas as pd
from emoji import emojize

from report_util.email_util import login_smtp_send_mail

__author__ = 'Jam'
__date__ = '2019/4/25 11:25'


def product(a, b):
    return a * b


def argument_unpacking():
    argument_tuple = (1, 1)
    argument_dict = {'a': 1, 'b': 1}

    print product(*argument_tuple)
    print product(**argument_dict)


def boolasint(a):
    print(isinstance(a, int) + (a <= 10))
    print(["is odd", "is even"][a % 2 == 0])

    print(True + True, True + False)
    print(["is odd", "is even"][True])
    print(["is odd", "is even"][False])


def dict_calculator():
    import operator
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "/": operator.truediv,
        "*": operator.mul
    }

    print (ops['+'](50, 25))


def chaincompare():
    a = 10
    print(1 < a < 50)
    print(10 == a < 20)
    print(11 == a < 20)


def compile_(s):
    code = """def f(x):\n  return {}""".format(s)
    scope = {"sin": math.sin, "cos": math.cos, "sqrt": math.sqrt}
    exec (code, scope)

    return scope["f"]


def flattenlist():
    a = [[1, 2], [3, 4, ]]

    print(list(itertools.chain(*a)))

    print(list(itertools.chain.from_iterable(a)))

    print(sum(a, []))


def get_max_min_index():
    lst = [40, 10, 20, 30]
    print(minIndex(lst))
    print(maxIndex(lst))


def minIndex(lst):
    return min(range(len(lst)), key=lst.__getitem__)


def maxIndex(lst):
    return max(range(len(lst)), key=lst.__getitem__)


class Person:
    pass


def format_code():
    a = {'name': 'Jam', 'age': 18}
    print("My name is %(name)s and I'm %(age)i years old." % a)

    b = {'name': 'Jam', 'age': 18}
    print("My name is {name} and I'm {age} years old.".format(**b))

    c = {'email': 'Jam@usr.com', 'phone': '919-123-4567'}
    print('My name is {0[name]}, my email is {1[email]} and my phone number is {1[phone]}'.format(b, c))

    me = Person()
    me.name = 'Jam'
    me.email = 'Jam@usr.com'
    me.phone = '919-123-4567'
    print type(me)
    print('My name is {me.name}, my email is {me.email} and my phone number is {me.phone}'.format(me=me))


def transpose():
    original = [['a', 'b'], ['c', 'd'], ['e', 'f']]
    transposed = zip(*original)
    print(list(transposed))


def tree():
    from collections import defaultdict

    tree = lambda: defaultdict(tree)

    users = tree()
    users['harold']['username'] = 'chopper'
    users['matt']['password'] = 'hunter2'
    print users


def print_test(a, b):
    print a, b


def test_split():
    account = '18186143481 ls19910924!'
    print_test(*account.split())


def test_dict():
    a = {'a': {}}
    print a
    print a['a']
    print len(a['a'])
    print isinstance(a['a'], dict)
    if len(a['a']) == 0:
        a['a'] = ''
        print a


def test_exit(is_exit=True):
    if is_exit:
        exit(-1)

    print 1212
    return 1


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def tets_pop3_email():
    host = 'partner.outlook.cn'
    username = 'jaliang@capvision.com'
    password = 'ls19910924!'
    conn = poplib.POP3_SSL(host)
    conn.user(username)
    conn.pass_(password)
    mail_total, total_size = conn.stat()

    mail = conn.retr(mail_total)[1]
    msg = Parser().parsestr('\r\n'.join(mail))

    header_dict = dict()
    for header in ['From', 'To', 'Subject', 'Cc', 'Bcc', 'Content-Type', 'Message-ID']:
        if header == 'Subject':
            header_dict[header] = decode_str(msg.get(header, ''))
        else:
            header_dict[header] = msg.get(header, '')

    print header_dict
    print decode_header(header_dict['Content-Type'])
    charset = msg.get_charset()
    print charset

    charset_content = msg.get_content_type()
    print charset_content

    for part in msg.walk():
        if not part.is_multipart():
            filename = part.get_filename()
            content = part.get_payload(decode=True)
            charset = part.get_content_charset()

            if filename:
                break

            clean_content = html2text.html2text(content.strip())

            print charset, filename
            print clean_content
        else:
            print 'Multipart do not parse.'


import re


def test_regex():
    pattern = re.compile(u"\\[(.*?)期\\]")
    match = pattern.search(u'期刊[10期]')

    if match:
        print match.group(1)


def test_modify():
    print 6.5 / 2
    print int(6.5 / 2)
    print int(6.5 // 2)

    test_list = [1, 2, 3, 4, 5]

    print test_list[1]
    print test_list[int(6.5 / 2)]


def tuple_cmp():
    tuple1 = (1, 'a')
    tuple2 = (1, 'b')
    tuple3 = (2, 'a')

    print tuple1 < tuple2
    print tuple1 < tuple3


def test_shufft():
    test_list = range(20)
    random.shuffle(test_list)
    print test_list


def test_sum():
    list_1 = [1, 2, 3, 4, 5]
    list_total = [list_1, [num * 2 for num in list_1]]
    print list_total

    df = pd.DataFrame(list_total)

    print df

    print df.items
    print df.columns
    print df.index

    print df[0].sum()
    print df[1].mean()


def test_zip_multi():
    list1 = [1, 2, 3]
    list2 = [(1, 2), (2, 4), (3, 6)]

    for a, b in zip(list1, list2):
        print a, b


def test_environment():
    os.environ['MODE'] = 'PRO'
    servers = [
        ["pipenv", "run", "gunicorn", "-c", "config/gunicorn.py", "--worker-class", "sanic.worker.GunicornWorker",
         "server:app"],
        ["pipenv", "run", "python", "scheduled_task.py"]
    ]

    print type(os.environ)

    print json.dumps(dict(os.environ), indent=4, sort_keys=True)


def test_string_count():
    title = 'asasasas'
    print  title.count('a')


def test_beep_sound():
    winsound.Beep(600, 1500)


def test_reverse():
    for item in reversed(range(-10, 1)):
        print item


def test_update():
    test_dict = {k: 0 for k in [1, 2, 3, 4, 5]}
    test_dict.update({1: 2, 2: 6})
    print test_dict
    print  sorted(test_dict.items(), key=lambda xx: xx[1], reverse=True)


def get_industry_set():
    INDUSTRY_LIST = [
        u"交通运输",
        u"房地产",
        u"电子",
        u"家用电器",
        u"家电",
        u"钢铁",
        u"医药",
        u"国防军工",
        u"电气设备",
        u"公用事业",
        u"纺织服装",
        u"计算机",
        u"机械",
        u"有色",
        u"银行",
        u"通信",
        u"机械设备",
        u"食品饮料",
        u"地产",
        u"商业贸易",
        u"农林牧渔",
        u"建筑",
        u"交运",
        u"旅游",
        u"服务",
        u"农业",
        u"休闲服务",
        u"汽车",
        u"轻工",
        u"建筑材料",
        u"采掘",
        u"建筑装饰",
        u"化工",
        u"医药生物",
        u"有色金属",
        u"商贸",
        u"金融",
        u"食品",
        u"纺织",
        u"公用",
        u"传媒",
        u"交通",
        u"非银金融",
        u"轻工制造",
        u"综合",
    ]

    industry_list2 = [
        u'交运',
        u'化工',
        u'医药',
        u'地产',
        u'家电',
        u'建筑',
        u'旅游',
        u'有色',
        u'机械',
        u'电子',
        u'采掘',
        u'金融',
        u'钢铁',
        u'食品',
        u'农业',
        u'计算机',
        u'纺织',
        u'轻工',
        u'公用',
        u'交通',
        u'商贸',
        u'旅游',
        u'服务',
        u'综合',
    ]

    for industry in set(INDUSTRY_LIST):
        if industry not in industry_list2:
            print "u" + "\"" + industry + "\"" + ","


def test_pandas_properity():
    data = {'id': range(10),
            'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat', 'dog', 'dog'],
            'age': [2.5, 3, 0.5, 1, 5, 2, 4.5, 1, 7, 3],
            'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
            'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}

    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    df = pd.DataFrame(data, index=labels)
    print df

    target_movies = list(df[df['id'] == 1]['animal'])
    other_users_id = list(int(i) for i in set(df['id']) if i != 1)
    print target_movies
    print other_users_id

    df['priority'] = df['priority'].replace(['yes', 'no'], [1, 0])
    print df


def test_random():
    data = list(range(100))
    print int(len(data) / 2)
    print random.randint(0, int(len(data) / 2))


def error_request(num):
    data = {"flag": num}
    result = {"message": "failed", "data": data}
    result = json.dumps(result)
    print result, type(result)


def success_request(num):
    data = {"flag": num}
    result = {"message": "success", "data": data}
    result = json.dumps(result)
    print result, type(result)


def create_random_token():
    tooken = "test_jam"
    time_str = str(int(time.time()))
    tooken = hashlib.md5((tooken + time_str)).hexdigest()
    print  tooken, len(tooken)

    start_num = random.randint(0, (len(tooken) - 20))
    print start_num
    token = str(tooken)[start_num:(start_num + 20)]
    print  token


def request_test():
    import requests

    url = "http://www.mims.com.cn/china/drug/info/999%20piyanping/"

    querystring = {"type": "brief"}

    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Referer': "http://www.mims.com.cn/Captcha/DefaultCaptcha?returnUrl=http%3a%2f%2fwww.mims.com.cn%2fchina%2fdrug%2finfo%2flin%2520mai%2520xin%2f",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'Cookie': "_ga=GA1.3.1880511766.1560997854; __gads=ID=5b6125657704b69f:T=1560997863:S=ALNI_MZFIJ663LWp1z-zZXEYjnHVcm5ibA; _daxbypass=true; ARRAffinity=e500cbac8b9ba7c771194151aa62dfc71e898319a9963cf65c5b7419cc339df9; ASP.NET_SessionId=r2kq1cki4wv0kfcxq14r2gwz; _gid=GA1.3.951321368.1561601668; MIMSV2.AUTH.2=D6CF66F6A4D3011314B4611D3F9E3E2464702AA103F83CF23CE9888C0DD8DB8769654B54596D38E470A538BE3EC29349A1B15732C48DE26A2CC7A5674DA2778146B10D11C304D95E1B1E483DD2C3115F3405F4EF0742DDE1F13F5D449BCB21030BF1B8DE3D09F7671377AA9E7EBA0BE46C87FA8043BD3959C7EF1DE4CD7A1215680FE83C5ACC8DF7379B74D81276D0801F22545F5CE64DB891B115D5A2984D6AE42FD431E19C8FA5774994A68CCDF894E7C1E1B086682D912A4AB1694A9BFE69D119D0AD9B0DA7596E9381852EDAF9769432B3D0441598CE73352DA6DF304A654FA4911410514C8A6F2940A259DFBEB391E6EDB8C51AF7BC7EA0E7A47788791F40F61627FA10617803644CF696030F6DC0E5FDE7F9F648AF7A9B85700651A26C926BB207C00B5B37C7F9D563C657BEEA1A4C3E8AC6278CBA957AD50B937DE2A4126EBAF7935AE130A16F5DB13DDAE32647134937AA2ADE106FE8893CB77E06D3F4D2F9D2B280B5D51D191893E0DDDDF0C4C825EF5483C3BFFDE80ADB6395E74E1153DCA5909153D7C692524F446C47937CE44C0D0352B62186E26047201857F1",
        'Postman-Token': "31fa1ad4-8d69-4e28-90f4-976ac47b542f,d2653fa2-3572-423e-9f68-48ac7d2857d1",
        'Host': "www.mims.com.cn",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


def remove_even_index():
    num_list = range(20)
    even_num = num_list[::2]
    del num_list[::2]
    print num_list, even_num


def test_while_else():
    n = 10
    while (n - 1) > 0:
        print n
        n -= 1
        raise Exception('test else')
    else:
        print 'test else'


def test_for_else():
    for num in range(10):
        print num
        raise ValueError('test else')
    else:
        print 'test else'


def test_namedtuple():
    import doctest
    TestResults = namedtuple('TestResults', 'failed attempted')
    print doctest.testmod()
    print TestResults(*doctest.testmod())


def test_group_split():
    data = {'id': range(10),
            'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat', 'dog', 'dog'],
            'age': [2.5, 3, 0.5, 1, 5, 2, 4.5, 1, 7, 3],
            'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
            'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}

    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    df = pd.DataFrame(data, index=labels)
    print df

    for name, sole in df.groupby("animal"):
        print name, sole['visits'].min(), sole['visits'].max()


def test_emoji():
    print emojize(":thumbs_up:")


def test_inspect():
    import inspect
    print inspect.getsource(inspect.getsource)
    print inspect.getmodule(inspect.getmodule)
    print inspect.currentframe().f_lineno


def test_uuid():
    # Universally Unique IDentifier
    user_id = uuid.uuid4()
    print user_id


def test_float_int_cmp():
    print  0.66 > 0


def read_dr_table():
    df = pd.read_excel('./data/Daily report_temp.xlsx', sheet_name='Summary new', skiprows=3, usecols='C:H')
    df = df.drop([1, 10, 11]).fillna('')
    df['Completion against Budget'] = df['Completion against Budget'].apply(
        lambda xx: '{}%'.format(str(round(xx * 100, 2))) if xx else '')

    cols_round = ['Openning', 'Today', 'MTD']
    df[cols_round] = df[cols_round].applymap(lambda xx: str(int(xx)) if xx or xx == 0 else '')
    df['budget'] = df['budget'].apply(lambda xx: int(xx) if xx else '')
    print df
    print  df.values.tolist()


def test_email_table():
    df = pd.read_excel('./data/Daily report_temp.xlsx', sheet_name='Summary new', skiprows=3, usecols='C:H')
    df = df.drop([1, 10, 11]).fillna('')
    df['Completion against Budget'] = df['Completion against Budget'].apply(
        lambda xx: '{}%'.format(str(round(xx * 100, 2))) if xx else '')

    cols_round = ['Openning', 'Today', 'MTD']
    df[cols_round] = df[cols_round].applymap(lambda xx: str(int(xx)) if xx or xx == 0 else '')
    df['budget'] = df['budget'].apply(lambda xx: int(xx) if xx else '')

    content_list = df.values.tolist()

    email_config = dict(
        smtp="smtp.partner.outlook.cn",
        email_address="dbsender@capvision.com",
        password="1qaz@WSX",
        to=["jaliang@capvision.com", ""],
        title="Github Top25 Of Python",
    )

    email_template = '''
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>Github Top25 Of Python</title>
        </head>
        <body>
            <table align="center" color="#f2e1c9" border="0" cellpadding="0" cellspacing="0" style="width: 40%;">
                <tr>
                    <td>
                        <table class="content" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                            <th style="width: 10%;text-align:left">Daily Status {date} RMB</th>
                            <th style="width: 8%;text-align:right">Openning</th>
                            <th style="width: 8%;text-align:right">Today</th>
                            <th style="width: 8%;text-align:right">MTD</th>
                            <th style="width: 8%;text-align:right">Budget</th>
                            <th style="width: 8%;text-align:center">Completion against Budget</th>
                        </tr>
                        {table_content}
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    '''

    msg = MIMEMultipart()
    msg["Subject"] = email_config.get('title')
    msg["From"] = email_config.get('email_address')
    msg["To"] = email_config.get('to')
    to_addrs = email_config.get('to').split(',')

    table_content = ""
    for index, item in enumerate(content_list, 1):
        if index == 1:
            table_content += '''<tr><td style="width: 20%;text-align:left;background-color:yellow">{}</td>
                                    <td style="width: 16%;text-align:right;background-color:yellow">{}</td>
                                    <td style="width: 16%;text-align:right;background-color:yellow">{}</td>
                                    <td style="width: 16%;text-align:right;background-color:yellow">{}</td>
                                    <td style="width: 16%;text-align:right;background-color:yellow">{}</td>
                                    <td style="width: 16%;text-align:center;background-color:yellow">{}</td>
                                </tr>'''.format(
                item[0], item[1], item[2], item[3], item[4], item[5]
            )
        else:
            table_content += '''<tr><td style="width: 20%;text-align:left">{}</td>
                                    <td style="width: 16%;text-align:right">{}</td>
                                    <td style="width: 16%;text-align:right">{}</td>
                                    <td style="width: 16%;text-align:right">{}</td>
                                    <td style="width: 16%;text-align:right">{}</td>
                                    <td style="width: 16%;text-align:center">{}</td>
                                </tr>'''.format(
                item[0], item[1], item[2], item[3], item[4], item[5]
            )

    mail_template = email_template.format(
        table_content=table_content,
        date='2019-07-01'
    )
    print mail_template

    content = MIMEText(mail_template, 'html', 'utf-8')
    msg.attach(content)

    login_smtp_send_mail(email_config, to_addrs, msg)


def check_industry_set():
    INDUSTRY_LIST = [
        "000338", "000951", "002078", "002126", "002191", "002572", "002595", "002791", "002833", "300415", "600004",
        "600009", "600031", "600660", "600699", "600761", "601238", "601689", "603337", "603338,603899"
    ]

    industry_list2 = [
        "000338", "600031", "000951", "002078", "002126", "002191", "002572", "002595", "002791", "002833", "002367",
        "300415", "600009", "600004", "600660", "600699", "603338", "600761", "601238", "601689", "603305", "600104",
        "603337", "603899", "603833", "000786", "601877", "603583"
    ]

    for industry in set(industry_list2):
        if industry not in INDUSTRY_LIST:
            # print "u" + "\"" + industry + "\"" + ","
            print industry


def test_commo():
    num = '118,939.00'
    print(float(re.sub(r',', '', str(num)).replace('-', '')))


def test_str_enumer():
    new = []
    val = '-aasasa-s'
    print(val.count('-'), val.count(','))
    for index, elem in enumerate(val):
        if elem == '-' and index > 0:
            elem = ''

        new.append(elem)

    print(''.join(new))


def test_random_():
    A = random.randint(10, 20)
    print(A)
    print(2 * A)


def make_tree_dict():
    from collections import defaultdict

    tree = lambda: defaultdict(tree)

    users = tree()
    users['harold']['username'][1] = 'chopper'
    users['matt']['password'][2] = 'hunter2'
    for index, item in users.iteritems():
        print(index, item)


def sorted_list():
    l = [4, 2, 3, 5, 1]
    print("original list: ", l)

    values, indices = zip(*sorted((a, b) for (b, a) in enumerate(l)))

    print("sorted list: ", values)
    print("original indices: ", indices)


def remove_dul():
    from collections import OrderedDict

    items = ["foo", "bar", "bar", "foo"]
    print(list(set(items)))
    print(dict(OrderedDict.fromkeys(items)))

    print(list(OrderedDict.fromkeys(items).keys()))


def test_time():
    t1 = time.time()
    time.sleep(10)
    t2 = time.time()
    print t1, t2, t2 - t1


def check_valid():
    frequency_num = 101
    frequency_num_check = frequency_num <= 100
    print frequency_num_check
    print not None


def test_enco__():
    password = 'asdf1234!'
    sha256 = hashlib.sha256(bytes('加一些东西') + b'lxgzhw')
    sha256.update(bytes(password))
    password = sha256.hexdigest()
    print password


def django_enco__():
    from django.contrib.auth.hashers import make_password, check_password

    import os, django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

    passwd1 = make_password("asdf1234!")
    passwd2 = make_password("asdf1234!", None, 'pbkdf2_sha256')

    print passwd1
    print passwd2
    check_valid = check_password("asdf1234!",
                                 "pbkdf2_sha256$36000$SQUOTrcBe4by$z430V6mFvdF4me+42LKHYzfhYgn+qVybttX7QtvwTyU=")
    print check_valid


def create_db_uri():
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'quant'

    DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                DATABASE)
    print DATABASE_URI


import ahocorasick


def test_ahcorasick():
    A = ahocorasick.Automaton()

    titles = ['Hello Kitty3色蔬菜细面300克 婴儿幼儿营养面条宝宝辅食面条']

    word_dict = {}

    with open('categories.csv', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            word_key = line.split(':')[0]
            word_value = list(line.split(':')[1].split('|'))
            word_dict[word_key] = word_value
            line = (line.split(':')[1].split('|'))
            for word in line:
                if word == "":
                    continue
                A.add_word(word, word)

    A.make_automaton()

    for title in titles:
        category = []
        aa = A.iter(title)
        ret = []
        matches = {}

        for (k, v) in aa:
            matches[v] = 1

        for (k, v) in matches.items():
            ret.append(k)

        for value in word_dict.items():
            if ret[0] in value[1]:
                category.append(value[0])
                # print(ret[0], value[0], value[1])
        print(category[0])


def __test_split():
    string_test = {'好    很好', '行  还行'}
    wors_dicts = {word.split(' ')[0]: word.split(' ')[-1] for word in string_test}

    print wors_dicts.keys()[0], wors_dicts.values()[0]


def custom_len(value):
    # These characters take up more space
    characters = {
        '进': 2,
        '度': 2,
    }

    total = 0
    for c in value:
        total += characters.get(c, 1)

    return total


def show_process_bar():
    import time
    import progressbar
    bar = progressbar.ProgressBar(
        widgets=[
            '进度: ',
            progressbar.Bar(),
            ' ',
            progressbar.Counter(format='%(value)02d/%(max_value)d'),
        ],
        term_width=custom_len,
    )
    for i in bar(range(10)):
        time.sleep(0.1)


def parse_query(url):
    result = urlparse(url)
    print(result)
    query = result.query
    print(query)
    query_dict = parse_qs(query)
    print(query_dict)
    query_dict = {k: v[0] for k, v in query_dict.items()}
    print(query_dict)
    return query_dict


def parse_datetime(string):
    import dateparser

    if not string:
        return None

    print(dateparser.parse(str(string)))
    return dateparser.parse(str(string))


def bool_test():
    print(bool([]))


def tets_jieba():
    import jieba.posseg as psg
    text = u'欧阳建国是创新办主任也是欢聚时代公司云计算方面的专家'
    for text_seg in psg.cut(text):
        if text_seg.flag.startswith('n'):
            print text_seg.word,text_seg.flag



if __name__ == "__main__":
    tets_jieba()
