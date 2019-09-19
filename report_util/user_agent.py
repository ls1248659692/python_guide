#!/usr/bin/python
# coding=utf8
import random

__author__ = 'Jam'
__date__ = '2018/12/10 11:51'

def get_user_agent():
    user_agent_list = []
    f = open('../static/user_agent/user_agent.txt','r')
    for date_line in f:
        user_agent_list.append(date_line.replace('\r\n',''))
    # now_ua =  random.choice(user_agent_list)
    for  user_agent in user_agent_list:
        print '"'+user_agent.strip()+'"',','



if __name__ == '__main__':
    get_user_agent()



