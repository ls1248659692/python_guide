# coding:utf-8
# !/usr/bin/env python
import os

import records
import pandas as pd

from report_log import report_log
from report_py.constant import PathConst

PROJECT = os.path.dirname(os.path.realpath(__file__))
log = report_log.ReportLog()


def check_fdir(path):
    fdir = os.path.join(path)
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    return fdir


def dataframe_to_excel(filename, excel_info_list):
    fdir = check_fdir(PathConst.DB_REPORT_PATH)

    writer = pd.ExcelWriter(fdir + filename, engine='xlsxwriter')
    workbook = writer.book
    head_format = workbook.add_format(
        {
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'calibri',
            'bold': True,
            'font_size': 12})

    cell_format = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'font_name': 'calibri', 'font_size': 11
    })

    float_format = workbook.add_format(
        {
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'calibri',
            'num_format': '#,###,##0.00',
            'font_size': 11})

    for sheet in excel_info_list:
        sheetname, data = sheet['sheetname'], sheet['data']
        cols_width_dict, float_cols_list = sheet['cols_format']['cols_width'], sheet['cols_format']['float_cols']
        data.to_excel(writer, sheetname, index=False, header=False)

        worksheet = writer.sheets[sheetname]
        worksheet.write_row(0, 0, data.columns.values, head_format)

        if cols_width_dict:
            for key, value in cols_width_dict.items():
                worksheet.set_column(key, value, cell_format)

        if float_cols_list:
            for float_col in float_cols_list:
                worksheet.set_column(float_col, 10, float_format)

    writer.save()

    return (fdir + filename)


def sql_to_excel(filename, db_url, sql_path):
    fdir = check_fdir(PathConst.DB_REPORT_PATH)

    db = records.Database(db_url)
    rows = db.query_file(sql_path)
    with open(fdir + filename, 'wb', ) as f:
        f.write(rows.export('xls'))
    # print(rows.dataset)
    db.close()

    return (fdir + filename)


