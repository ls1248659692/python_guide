#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2018/12/4 11:26'


# ---------------------------------------------------------------------------------------------------------------
MONGODB_CONFIG = {
    'host': '192.168.5.220',
    'port': 27017,
    'username': None,
    'password': None
}

MYSQL_CONFIG_95 = {
    'host': '192.168.50.95',
    'port': 3306,
    'user': "admin",
    'passwd': "admin2048az",
    "db": 'test',
    "charset": 'utf8',
}

MYSQL_CONFIG_87 = {
    'host': '192.168.5.87',
    'port': 3306,
    'user': "admin",
    'passwd': "admin1234",
    "db": 'test',
    "charset": 'utf8',
}

MYSQL_CONFIG_73 = {
    'host': '121.40.69.73',
    'port': 9916,
    'user': "root",
    'passwd': "admin1234",
    "db": 'quant',
    "charset": 'utf8',
}

MYSQL_CONFIG_254 = {
    'host': '47.52.132.254',
    'port': 9916,
    'user': "admin_sup",
    'passwd': "qwer1234!",
    "db": 'quant',
    "charset": 'utf8',
}

EXCEPTION_INFO = '''
<div class="emailcontent" style="width:100%;max-width:720px;text-align:left;margin:0 auto;padding-top:80px;padding-bottom:20px">
    <div class="emailtitle">
        <div class="emailtext" style="background:#fff;padding:20px 32px 20px">
            <table cellpadding="0" cellspacing="0" border="0" style="width:100%;border-top:1px solid #eee;border-left:1px solid #eee;color:#6e6e6e;font-size:16px;font-weight:normal">
                <thead>
                    <tr>
                        <th colspan="2" style="padding:10px 0;border-right:1px solid #eee;border-bottom:1px solid #eee;text-align:center;background:#f8f8f8"><b> web_name - {web_name}, process - {process_type} </b></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding:10px 0;border-right:1px solid #eee;border-bottom:1px solid #eee;text-align:center;width:100px">异常简述</td>
                        <td style="padding:10px 20px 10px 30px;border-right:1px solid #eee;border-bottom:1px solid #eee;line-height:30px">{error_reason}</td>
                    </tr>
                    <tr>
                        <td style="padding:10px 0;border-right:1px solid #eee;border-bottom:1px solid #eee;text-align:center">异常详情</td>
                        <td style="padding:10px 20px 10px 30px;border-right:1px solid #eee;border-bottom:1px solid #eee;line-height:30px">{error_detail}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
'''

PROCESS_TYPE_DICT = {
    0: "request",
    1: "generate data",
    2: "download data",
    3: "upload data"
}
