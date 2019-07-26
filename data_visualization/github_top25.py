#!/usr/bin/python
# coding=utf8
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests

from bs4 import BeautifulSoup

from pyquery import PyQuery as pq

from data_visualization.constant import GitHubData
from report_util.email_util import login_smtp_send_mail

__author__ = 'Jam'
__date__ = '2018/12/25 16:53'


##  自动提交代码到 git
def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def scrape(language):
    response = requests.get(
        GitHubData.TOP25_URL.format(language=language),
        headers=GitHubData.HEADERS
    )

    if response.status_code == 200 and response.content:
        d = pq(response.content.decode('utf-8', 'ignore'))
        items = d('div.explore-pjax-container .Box-row')

        result = []
        for item in items:
            i = pq(item)
            title = i("h1 a").text().split('/')[-1].strip()
            description = i("p.col-9").text()
            url = i("h1 a").attr("href")
            url = "https://github.com" + url
            result.append([title, url, description])

        return result
    else:
        print GitHubData.ERROR_MSG.format(response.status_code)


def send_mail(content_list):
    email_config = GitHubData.EMAIL_CONFG

    msg = MIMEMultipart()
    msg["Subject"] = email_config.get('title')
    msg["From"] = email_config.get('email_address')
    msg["To"] = email_config.get('to')
    to_addrs = email_config.get('to').split(',')

    table_content = ""
    for index, item in enumerate(content_list, 1):
        table_content += '''<tr><td>&nbsp;{}&nbsp;</td><td>{}</td><td>{}</td><td>{}</td></tr>'''.format(
            index, str(item[0]), str(item[1]), item[2].encode('utf-8')
        )

    mail_template = GitHubData.MAIL_TEMPLATE.format(
        table_content=table_content
    )

    content = MIMEText(mail_template, 'html', 'utf-8')
    msg.attach(content)

    login_smtp_send_mail(email_config, to_addrs, msg)


class GitHub():
    def __init__(self):
        self.session = requests.session()
        self.timeline = []
        self.name = ''
        self.user = ''
        self.passwd = ''

    def login(self):
        html = self.session.get(
            'https://github.com/login',
            headers=GitHubData.GITHUB_HEADER
        ).text

        authenticity_token = BeautifulSoup(html, 'lxml').find(
            'input', {'name': 'authenticity_token'}
        ).get('value')

        data = {
            'commit': "Sign in",
            'utf8': "✓",
            'login': GitHubData.USERNAME,
            'password': GitHubData.PASSWORD,
            'authenticity_token': authenticity_token
        }

        html = self.session.post('https://github.com/session', data=data, headers=GitHubData.GITHUB_HEADER).text
        self.name = BeautifulSoup(html, 'lxml').find(
            'strong', {'class': 'css-truncate-target'}
        ).get_text()

    def get_timeline(self, page=1):
        html = self.session.get(
            'https://github.com/dashboard/index/{page}?utf8=%E2%9C%93'.format(page=page),
            headers=GitHubData.GITHUB_HEADER
        ).text

        table = BeautifulSoup(html, 'lxml').find(
            'div', id='dashboard'
        ).find_all(
            'div', {'class': 'alert'}
        )

        for item in table:
            line = dict()
            line['thing'] = item.find('div', {'class': 'title'}).get_text(
            ).replace('\r', '').replace('\n', '')
            line['time'] = item.find('relative-time').get('datetime')
            self.timeline.append(line)

    def show_timeline(self):
        for line in self.timeline:
            text = line['time'] + ' ' + line['thing']
            print '*' + text + ' ' * (80 - len(text) - 2) + '*'

    def overview(self, user=None):
        if user == None:
            user = self.name
        html = self.session.get(
            'https://github.com/' + user,
            headers=GitHubData.GITHUB_HEADER
        ).text

        ## need to extract data
        return html


def main():
    result = scrape('Python')
    send_mail(result)


if __name__ == '__main__':
    main()
