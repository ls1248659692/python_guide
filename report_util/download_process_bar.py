# coding:utf-8
# !/usr/bin/env python

import sys
import time



def print_process_bar(download_name, lenth=50):
    sys.stdout.write(u"开始下载 %s" % download_name + '\r')
    time.sleep(1)

    for num in range(lenth):
        sys.stdout.write(u"正在下载 %.2f%%" %
                         ((float(num + 1) / lenth) * 100) + '\r')
        sys.stdout.flush()
        time.sleep(0.01)

    print(u"下载完成 %s" % download_name + '\r')


class ShowProcessBar:
    def __init__(self, max_steps, info_done='Done', max_arrow=50):
        self.max_steps = max_steps
        self.current_num = 0
        self.info_done = info_done
        self.max_arrow = max_arrow

    def show_process(self, current_num=None):
        if current_num is not None:
            self.current_num = current_num
        else:
            self.current_num += 1

        num_arrow = int(self.current_num * self.max_arrow / self.max_steps)
        num_line = self.max_arrow - num_arrow
        percent = self.current_num * 100.0 / self.max_steps

        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']' + '%.2f' % percent + '%' + '\r'

        sys.stderr.write(process_bar)
        time.sleep(0.01)

        if self.current_num >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.info_done)


if __name__ == '__main__':
    max_steps = 200

    process_bar = ShowProcessBar(max_steps, 'OK')

    for current_num in range(max_steps):
        process_bar.show_process()
