#!/usr/bin/python
# coding=utf-8
import os
import httplib
import mimetypes
import urlparse
import json
import time
from aip import AipOcr

APP_ID = '14734567'
API_KEY = 'aGlONgH43P4bchj53T8S6BcS'
SECRET_KEY = '1miW1gl4hlAhGLcNRt38AWkHnY9oqey4'

CLIENT = AipOcr(APP_ID, API_KEY, SECRET_KEY)
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FILE_PATH = os.path.join(PROJECT_ROOT, 'static/captcha_image/example.jpg')


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def img_captcha_recognize():
    image = get_file_content(FILE_PATH)
    CLIENT.basicGeneral(image)

    options = {}
    options["language_type"] = "ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    results = CLIENT.basicGeneral(image, options)
    print (results)


def url_captcha_recognize():
    url = "https://login.sina.com.cn/cgi/pin.php?r=5352100&amp;s=0&amp;p=aliyun-96660b4d28878967e256a306412f8868e045"

    CLIENT.basicGeneralUrl(url)

    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    results = CLIENT.basicGeneralUrl(url, options)
    print (results)


class YDMHttp:
    # 错误代码请查询 http://www.yundama.com/apidoc/YDM_ErrorCode.html
    # 所有函数请查询 http://www.yundama.com/apidoc

    # 1. http://www.yundama.com/index/reg/developer 注册开发者账号
    # 2. http://www.yundama.com/developer/myapp 添加新软件
    # 3. 使用添加的软件ID和密钥进行开发，享受丰厚分成


    apiurl = 'http://api.yundama.com/api.php'

    # 用户名
    username = ''
    # 密码
    password = ''
    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appid = ''
    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appkey = ''
    filename = ''
    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype = 1004
    # 超时时间，秒
    timeout = 60

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        try:
            response = post_url(self.apiurl, fields, files)
            response = json.loads(response)
        except Exception as e:
            response = None
        return response

    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''


def post_url(url, fields, files=[]):
    urlparts = urlparse.urlsplit(url)
    return post_multipart(urlparts[1], urlparts[2], fields, files)


def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('Host', host)
    h.putheader('Content-Type', content_type)
    h.putheader('Content-Length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    print  (errcode, errmsg, headers)
    return h.file.read()


def encode_multipart_formdata(fields, files=[]):
    BOUNDARY = 'WebKitFormBoundaryJKrptX8yPbuAJLBQ'
    CRLF = '\r\n'
    L = []
    for field in fields:
        key = field
        value = fields[key]
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for field in files:
        key = field
        filepath = files[key]
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filepath))
        L.append('Content-Type: %s' % get_content_type(filepath))
        L.append('')
        L.append(open(filepath, 'rb').read())
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def identify(username, password, appid, appkey, filename, codetype, timeout):
    if (username == 'username'):
        print( '请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login()
        # print 'uid: %s' % uid

        # 查询余额
        balance = yundama.balance()
        print ('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout)
        print ('cid: %s, result: %s' % (cid, result))
        return result


def main():
    img_captcha_recognize()
    # url_captcha_recognize()
    pass


if __name__ == "__main__":
    main()
