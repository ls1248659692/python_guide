# coding:utf-8
# !/usr/bin/env python
import os
import sys
import traceback

import requests

from config import config
# from excel_util import check_fdir
from report_log import report_log
from report_py.constant import PathConst, LogConst, CrawlerConst, Misc
from report_util import email_util
from report_util.constant import EXCEPTION_INFO, PROCESS_TYPE_DICT
from report_util.date_util import getnowtimestr
from functools import wraps

log = report_log.ReportLog()
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def download_url_file(url, header, filename, download_path, params=None):
    # check_fdir(download_path)

    response = requests.get(
        url, headers=header, stream=True, params=params
    )

    with open(download_path + filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=10000):
            file.write(chunk)
            file.flush()

    return response.status_code


def email_download_url_error(error_reason, process_type, web_name, error_detail=None):
    process_error = {
        0: CrawlerConst.REQUEST_STATUS_ERROR,
        1: CrawlerConst.GENERATE_DATA_ERROR,
        2: CrawlerConst.DOWNLOAD_DATA_ERROR,
        3: CrawlerConst.UPLOAD_DATA_ERROR
    }.get(process_type, Misc.PROCESS_TYPE_DEFAULT)

    log.printlog(
        LogConst.OTHER, process_error % dict(e=error_reason)
    )

    email_config = config.parse_crawler_configure(
        os.path.join(PROJECT_ROOT, PathConst.CONFIGURE_PATH)
    )

    email_config['title'] = "{today} : web crawler {web_name} occurs exception".format(
        today=getnowtimestr(),
        web_name=web_name
    )

    email_config['content'] = EXCEPTION_INFO.format(
        web_name=web_name,
        process_type=PROCESS_TYPE_DICT[process_type],
        error_reason=error_reason,
        error_detail=error_detail if error_detail is not None  else ''
    )

    email_util.send_mail(email_config)


def convert_df_to_file(df, download_path, file_name, columns_rank=None):
    # check_fdir(download_path)
    columns_rank = columns_rank if columns_rank else df.columns
    cols_not_find = [col for col in columns_rank if col not in df.columns]

    if cols_not_find:
        log.printlog(LogConst.OTHER, Misc.COLS_NOT_FIND %
                     dict(cols=','.join(cols_not_find)))
    else:
        df = df[columns_rank]

    filename = os.path.join(download_path, file_name)
    df.to_csv(filename)


def email_exception(*args1, **kwargs1):
    def wrapper(func):
        @wraps(func)
        def __deco(*args2, **kwargs2):
            try:
                result = func(*args2, **kwargs2)
                return result
            except Exception as e:
                process_type, web_name = args1

                email_download_url_error(
                    e, process_type, web_name,
                    error_detail="{}:{}".format(
                        func.__name__, traceback.format_exc()
                    )
                )

        return __deco

    return wrapper
