# coding:utf-8
# !/usr/bin/env python

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from report_log import report_log
from report_py.constant import LogConst

log = report_log.ReportLog()


def send_mail(email_config, attachment_path_list=''):
    if not isinstance(attachment_path_list, list):
        attachment_path_list = [attachment_path_list]

    msg = MIMEMultipart()
    msg["Subject"] = email_config.get('title')
    msg["From"] = email_config.get('email_address')
    msg["To"] = email_config.get('to')

    cc_addrs = list()
    if 'cc' in email_config:
        msg["Cc"] = email_config.get('cc')
        cc_addrs = email_config.get('cc').split(',')
    msg["Bcc"] = email_config.get('cc')
    bcc_addrs = email_config.get('bcc').split(',')
    to_addrs = email_config.get('to').split(',')
    to_addrs.extend(cc_addrs + bcc_addrs)

    content = MIMEText(email_config.get('content'), 'html', 'utf-8')
    msg.attach(content)

    for attachment_path in attachment_path_list:
        if attachment_path:
            attach_part = MIMEApplication(open(attachment_path, 'rb').read())
            attach_part.add_header(
                'Content-Type', 'application/octet-stream'
            )

            attach_part.add_header(
                'Content-Disposition',
                'attachment',
                filename=os.path.basename(attachment_path)
            )

            msg.attach(attach_part)

    # email send  retry only once
    try:
        login_smtp_send_mail(email_config, to_addrs, msg, debug=True)
        log.printlog(LogConst.OTHER, LogConst.EMAIL_SUCCESS %
                     dict(file_path=','.join(attachment_path_list)))
    except Exception as e:
        log.printlog(LogConst.OTHER, LogConst.EMAIL_ERROR % dict(e=e))
        login_smtp_send_mail(email_config, to_addrs, msg, debug=True)

    return True


def login_smtp_send_mail(email_config, to_addrs, msg, debug=False):
    try:

        if debug: log.printlog(LogConst.INFO, LogConst.INIT_SMTP_SUCCESS)

        smtp = smtplib.SMTP(
            email_config.get('smtp'),
            timeout=120
        )

        smtp.ehlo()
        smtp.starttls()
        smtp.login(
            email_config.get('email_address'),
            email_config.get('password')
        )

        if debug: log.printlog(LogConst.INFO, LogConst.LOGIN_SMTP_SUCCESS)
        smtp.sendmail(
            email_config.get('email_address'),
            to_addrs,
            msg.as_string()
        )
        smtp.quit()
        if debug: log.printlog(LogConst.INFO, LogConst.QUIT_SMTP_SUCCESS)

    except Exception as e:
        log.printlog(LogConst.OTHER, LogConst.EMAIL_ERROR % dict(e=e))
