#!/usr/bin/python
# coding=utf8
import time
import Queue
import threading

from flask import Flask

__author__ = 'Jam'
__date__ = '2018/11/30 16:10'

"""
Queue.Queue(maxsize=0)   FIFO， 如果maxsize小于1就表示队列长度无限
Queue.LifoQueue(maxsize=0)   LIFO，last in first out 如果maxsize小于1就表示队列长度无限
Queue.qsize()   返回队列的大小
Queue.empty()   如果队列为空，返回True,反之False
Queue.full()    如果队列满了，返回True,反之False
Queue.get([block[, timeout]])   读队列，timeout等待时间
Queue.put(item, [block[, timeout]])   写队列，timeout等待时间
Queue.queue.clear()   清空队列
"""
app = Flask(__name__)


def get_url(q, url):
    q.put(url)


def run_thread():
    theurls = ["http://www.baidu.com", "http://yahoo.com"]

    q = Queue.Queue()

    for u in theurls:
        t = threading.Thread(target=get_url, args=(q, u))
        t.daemon = True
        t.start()

    for _ in range(len(theurls)):
        s = q.get()  ##Queue.get（）默认是阻塞方式读取数据,由于队列的存在会一直存在优先顺序
        print s

    print "Done"


"""
如果子线程的daemon属性为False，主线程结束时会检测该子线程是否结束，如果该子线程还在运行，则主线程会等待它完成后再退出；
如果子线程的daemon属性为True，主线程运行结束时不对这个子线程进行检查而直接退出，同时所有daemon值为True的子线程将随主线程一起结束，而不论是否运行完成。
属性daemon的值默认为False，如果需要修改，必须在调用start()方法启动线程之前进行设置

理解网络请求时候的异步文件加载
web 同步mysql数据到redis的接口，因为数据同步涉及各种增删查改，如果用同步实现，可能回造成连接超时、堵塞
所以，使用python实现异步任务

"""


def print_number(number):
    time.sleep(0.01)
    print "Thread " + str(number) + " sleep for " + str(1) + " seconds"


def test_thread():
    t = threading.Thread(target=print_number, args=(1,))
    t.setDaemon(True)
    # t.setDaemon(False)
    t.start()
    print "thread end."
    # time.sleep(0.5)


@app.route("/")
def hello():
    test_thread()
    return "Hello World!"


if __name__ == '__main__':
    # run_thread()
    # test_thread()
    app.run(threaded=True)
