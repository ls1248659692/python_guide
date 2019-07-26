#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import sys
import subprocess
from subprocess import check_output

import psutil

from report_log import report_log
from constant import *
from  report_util.data_analysis_head import *

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config/config.ini')
log = report_log.ReportLog('monitor_process')


def ping(host):
    try:
        shell_output = check_output("ping {host} -n 2".format(host=host), shell=True)
    except:
        log.printlog(u'{host} network is error.'.format(host=host))
        return False

    if shell_output:
        result = True if u'无法访问'.encode('gbk') not in shell_output  else False
        log.printlog(u'{host} network is ok.'.format(host=host))
        return result


def get_processes_running():
    tasks = subprocess.check_output(['tasklist'])
    tasks = [task for task in str(tasks).split('\r\n') if task]

    process_list = []
    for task in tasks[1:]:
        result = re.match("(.+?)\s+(\d+)\s+(.+?)\s+(\d+)\s+(\d+.*?)\s.*", task)
        if result is not None:
            process_list.append(
                {
                    "image": result.group(1),
                    "pid": result.group(2),
                    "session_name": result.group(3),
                    "session_num": result.group(4),
                    "mem_usage": int(result.group(5).replace(',', ''))
                }
            )

    df = pd.DataFrame(process_list)
    df.sort_values('mem_usage', ascending=False, inplace=True)
    return df


def get_process_info(process_name):
    process_exe_map = {'jupyter.exe': 'jupyter notebook'}
    df = get_processes_running()

    if process_name in df['image'].unique():
        log.printlog(INFO, '{process_name} is running.'.format(process_name=process_name))
    else:
        log.printlog(WARNING, '{process_name} is restartting.'.format(process_name=process_name))
        os.system(r"{0}".format(process_exe_map.get(process_name, process_name)))


def get_comand_info(exe_image, process_name):
    df = get_processes_running()
    pid_list = df[df['image'].str.match(exe_image, re.I)].pid.tolist()
    python_pids = map(int, pid_list)

    comand_list = []
    for proc in psutil.process_iter():
        proc_dict = proc.as_dict()
        if int(proc_dict['pid']) in python_pids:
            comand_list.append(' '.join(proc_dict['cmdline']))

    command_str = ' '.join(comand_list)
    if process_name in command_str:
        log.printlog(INFO, '{0} {1} is running.'.format(exe_image, process_name))
    else:
        log.printlog(INFO, '{0} {1} is restartting.'.format(exe_image, process_name))
        os.system(r"{0} {1}".format(exe_image, process_name))


def run():
    filepath = 'D:/Jam/my_pythonfile/test_pandaspretty.py'
    ping('192.168.5.145')
    get_processes_running()

    # 程序具有唯一性
    get_process_info('jupyter.exe')

    # 程序不具有唯一性
    get_comand_info('python', filepath)


if __name__ == "__main__":
    run()
