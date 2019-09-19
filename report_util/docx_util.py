# coding:utf-8
# !/usr/bin/env python

import os
import time
from zipfile import ZipFile

from lxml import etree
from docxtpl import DocxTemplate

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
docx_filedir = os.path.join(PROJECT_ROOT, 'static/docx_document/docx_template/')
unzip_filedir = os.path.join(PROJECT_ROOT, 'static/docx_document/docx_unzip/')
invoice_filedir = os.path.join(PROJECT_ROOT, 'static/docx_document/docx_invoice/')


def docx_file_unzip(input_file, output_path):
    with ZipFile(input_file, 'r') as zip_file:
        for filename in zip_file.namelist():
            if filename in ('word/document.xml'):
                zip_file.extract(filename, output_path)


def parse_xml_document(file_path):
    # 解析 word/document.xml
    print (open(file_path).read().decode('utf-8'))
    doc_xml = etree.XML(open(file_path).read())

    for field in doc_xml.xpath('//w:t', namespaces=doc_xml.nsmap):
        print (field.text)


def modify_xml_document(file_path):
    # 修改 word/document.xml,并返回结果
    doc_xml = etree.XML(open(file_path).read())
    return doc_xml


def xml_file_zip(file_path, xml_file_path, output_file):
    zipin = ZipFile(file_path)
    doc_xml = modify_xml_document(xml_file_path)

    with ZipFile(output_file, 'w') as outzip:
        for fileinfo in zipin.infolist():
            if fileinfo.filename in ('word/document.xml'):
                outzip.writestr(
                    'word/document.xml',
                    etree.tostring(
                        doc_xml,
                        encoding='utf-8',
                        xml_declaration=True,
                        standalone=True))
            else:
                outzip.writestr(fileinfo, zipin.read(fileinfo))


def modify_docx_document(input_file, output_file):
    start_time = time.time()
    docx_template = DocxTemplate(input_file)

    context = {
        'invoice_id': '666666',
        'date': '2018-10-26',
        'capvision_invoice_to': u'罗兰贝格企业管理（上海）有限公司',
        'bill_to': 'Jam',
        'service_provided_by': 'test_fill_document',
        'place_of_incorporation': 'shanghai',
        'contact': '666',
        'phone': '136-6666-6666',
        'email': '1248659692@qq.com',
        'service_description': 'Lifting system components market_CON1809211647[CP4940]_overseas Sep',
        'capvision_hour_charged': ' 66.00',
        'amount': '666666.00',
        'vat_tax': '666.00',
        'total_payment': '6666666.00',
        'exchange_rate': '6.66',
        'contract_type': 'Pay after Usage',
        'contract_currency': 'RMB',
        'contract_price': '3200.00',
        'contract_size': '6666666.00',
        'hours_remaining': '66.66',
        'terms_of_payment': 'Payment should be due within 30 days upon receipt of the invoice.',
        'acct_name': u'凯盛融英信息科技（上海）股份有限公司',
        'acct_number': '4364 6073 8869',
        'bank_name': u'中国银行上海市江苏路支行',
        'bank_address': u'中国上海市长宁路279号',
        'swift_code': 'BKCHCNBJ300',
        'swift': 'BKCHCNBJ300',
        'cnap': '6666666',
        'tbl_contents': [
            {'date': '2018-09-24', 'user': u'袁嘉', 'project': 'Lifting system', 'company': u'神力索具集团',
             'position': u'总监', 'type': 'Phone', 'notes': 'free', 'charged_hours': '0.50', 'amount': '1600.00'},
            {'date': '2018-09-25', 'user': u'袁嘉', 'project': 'Lifting system', 'company': u'神力索具集团',
             'position': u'总监', 'type': 'Phone', 'notes': 'free', 'charged_hours': '0.50', 'amount': '1600.00'},
            {'date': '2018-09-26', 'user': u'袁嘉', 'project': 'Lifting system', 'company': u'神力索具集团',
             'position': u'总监', 'type': 'Phone', 'notes': 'free', 'charged_hours': '0.50', 'amount': '1600.00'},
        ],
        'sum_charged_hours': '1.50',
        'sum_amount': '4800.00',
        'vat': '288.00',
        'total_amount': '5088.00',
        'notes': 'Test for python by Jam 2018-10-26'
    }

    # for value in flatten(context):
    #     print value

    # 特殊字符的转换，xml里面会不显示
    char_entity_map = {'&': '&amp;', '<': '&lt;', '>': '&gt;'}
    for col in context:
        for key, value in char_entity_map.items():
            if col == 'tbl_contents':
                for num in range(len(context[col])):
                    for sub_col in context[col][num]:
                        context[col][num][sub_col] = context[col][num][sub_col].replace(
                            key, value)
            else:
                context[col] = context[col].replace(key, value)

    docx_template.render(context)
    docx_template.save(output_file)

    print ('taken time is {time}'.format(time=time.time() - start_time))


def flatten(obj, ignore_itmes=(str, bytes)):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, list):
                yield flatten(value)
            elif isinstance(value, dict):
                yield flatten(value)
            else:
                yield key, value
    elif isinstance(obj, (list, set)):
        for item in obj:
            if isinstance(item, list):
                yield flatten(item)
            elif isinstance(item, dict):
                yield flatten(item)
            else:
                yield item


def docx_convert_pdf(input_file, output_file):
    from win32com import client as wc
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(input_file)
    doc.SaveAs(output_file, 17)  # 17对应于pdf文件
    doc.Close()
    word.Quit()
    pass


def main():
    docx_template = os.path.join(docx_filedir, 'docx_template.docx')
    docx_xml = os.path.join(unzip_filedir, 'word/document.xml')
    invoice_docx = os.path.join(invoice_filedir, 'invoice_test.docx')
    invoice_pdf = os.path.join(invoice_filedir, 'invoice_test.pdf')
    # docx_file_unzip(docx_template, unzip_filedir)
    # parse_xml_document(docx_xml)
    # xml_file_zip(docx_template, docx_xml, invoice_docx)
    modify_docx_document(docx_template, invoice_docx)
    # docx_convert_pdf(invoice_docx, invoice_pdf)

    pass


if __name__ == '__main__':
    main()
