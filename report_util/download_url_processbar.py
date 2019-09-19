# coding:utf-8
# !/usr/bin/env python
import os
import sys
import time

import requests

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filedir = os.path.join(PROJECT_ROOT, 'static/download_url/')


class ProgressBar(object):
    def __init__(
            self,
            filename='',
            file_size_sum=0.0,
            run_status='download running',
            unit='KB',
            chunk_size=1024):
        super(ProgressBar, self).__init__()
        self.info = "[%s download process]: %s %.2f%s"
        self.filename = filename
        self.file_size_sum = file_size_sum
        self.chunk_size = chunk_size
        self.run_status = run_status
        self.unit = unit
        self.times = float(chunk_size) / 1024

    def __get_info(self):
        _info = self.info % (self.filename, self.run_status, (float(
            self.file_size_sum) / self.chunk_size) * self.times, self.unit)
        return _info

    def refresh(self, file_size=0, wait_time=0.1):
        self.file_size_sum += file_size
        sys.stdout.write(self.__get_info() + "\r")
        time.sleep(wait_time)


def download_url_processbar(url, filename=None):
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    filename = url.split('/')[-1] if filename is None  else filename
    chunk_size, wait_time = 1024 * 2, 0.1

    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            progress = ProgressBar(
                filename=u"{filename}".format(filename=filename),
                chunk_size=chunk_size
            )

            with open(filedir + filename, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    progress.refresh(file_size=len(data), wait_time=0.2)
                    file.write(data)
        else:
            print(u'the url is error,please check reason.o')


def main():
    url = 'http://www.csindex.com.cn/uploads/file/autofile/cons/000001cons.xls'
    download_url_processbar(url)
    pass


if __name__ == '__main__':
    main()
