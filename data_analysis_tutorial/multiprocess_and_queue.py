#!/usr/bin/python
# coding=utf8

import os
import re
import time
from multiprocessing import Process, Queue, Pool, Manager, Lock, Value

import requests

__author__ = 'Jam'
__date__ = '2018/11/30 9:47'

"""
多进程  共享  队列 multiprocessing.Process
逻辑:
   一个进程往队列写数据，一个进程从读写读数据
   写进程完了后，主进程与读进程一起退出

使用:
    1. 创建队列 q = multiprocessing.Queue() ,默认无限大小,可以指定大小
    2. 把队列 q 当参数传给 子进程 执行代码， 全局变量方式无法访问
    3. 在子进程中读写队列数据   q.put(<data>)  q.get()
"""


def write_error_page(quene, error_page):
    quene.put(error_page)
    print ('put page {0} to queue.'.format(error_page))


def get_page_num(quene):
    while 1:
        time.sleep(0.5)
        if quene.empty():
            print "mutilprocess is end."
            break
        else:
            page = quene.get()
            print ("get page {0} from queue.".format(page))


def run(error_page=20):
    quene = Queue()
    for page in range(10):
        quene.put(page)

    print "mutilprocess is start."
    pw = Process(target=write_error_page, args=(quene, error_page,))
    pr = Process(target=get_page_num, args=(quene,))
    pw.start()
    pr.start()
    pw.join()
    pr.join()


"""
多进程 生产者 消费者模型，使用队列实现 multiprocessing.Queue

逻辑:
    1个生产者，1个消费者在2个不同的进程中操作同一个队列
    生产者的速度是消费者的2倍，通过time.sleep(1)来进行速度的调整
"""


class producer(Process):
    def __init__(self, queue):
        Process.__init__(self)
        self.queue = queue

    def run(self):
        for page in range(10):
            self.queue.put(page)
            print "Producer: item %d appended to queue  and size of queue is %s. " % (page, self.queue.qsize())
            time.sleep(1)


class consumer(Process):
    def __init__(self, queue):
        Process.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            time.sleep(1)
            if self.queue.empty():
                print "mutilprocess is end."
                break
            else:
                time.sleep(1)
                page = self.queue.get()
                print "Consumer: item %d poped to queue." % page


def multiprocess_run():
    queue = Queue()

    process_producer = producer(queue)
    # time.sleep(1)  ## 等待生产，queue里面没有数据，不进行消费
    process_consumer = consumer(queue)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
    # process_consumer.terminate()   如果没有队列为空的判断，强制停止消费，避免队列为空发生阻塞


def get_page(url, pattern):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    }

    response = requests.get(url, headers=header)
    if response.status_code == 200:
        print response.text
        return (response.text, pattern)
    else:
        print response.status_code
        return


def parse_page(info):
    page_content, pattern = info
    res = re.findall(pattern, page_content)
    for item in res:
        print 'index', item[0]
        print 'url', 'http://maoyan.com' + item[1]
        print 'title', item[2]

        print 'actor', item[3].strip()[3:]
        print 'time', item[4][5:]
        print 'score', item[5], item[6]
        print


"""
同步方法apply()和map()返回值为函数的返回结果
1 p.apply(func [, args [, kwargs]]):在一个池工作进程中执行func(*args,**kwargs),然后返回结果。需要强调的是：此操作并不会在所有池工作进程中并执行func函数。如果要通过不同参数并发地执行func函数，必须从不同线程调用p.apply()函数或者使用p.apply_async()
2 p.apply_async(func [, args [, kwargs]]):在一个池工作进程中执行func(*args,**kwargs),然后返回结果。此方法的结果是AsyncResult类的实例，callback是可调用对象，接收输入参数。当func的结果变为可用时，将理解传递给callback。callback禁止执行任何阻塞操作，否则将接收其他异步操作中的结果。
3 p.close():关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成
4 P.jion():等待所有工作进程退出。此方法只能在close()或teminate()之后调用

异步方法apply_async()和map_async()的返回值是AsyncResul的实例obj。实例具有以下方法：
obj.get():返回结果，如果有必要则等待结果到达。timeout是可选的。如果在指定时间内还没有到达，将引发一场。如果远程操作中引发了异常，它将在调用此方法时再次被引发。
obj.ready():如果调用完成，返回True
obj.successful():如果调用完成且没有引发异常，返回True，如果在结果就绪之前调用此方法，引发异常
obj.wait([timeout]):等待结果变为可用。
obj.terminate()：立即终止所有工作进程，同时不执行任何清理或结束任何挂起工作。如果p被垃圾回收，将自动调用此函数
"""


def mutilpriocess_pool_run():
    pattern1 = re.compile(r'<dd>.*?board-index.*?>(\d+)<.*?href="(.*?)".*?title="(.*?)".*?star.*?>(.*?)<.*?releasetime.*?>(.*?)<.*?integer.*?>(.*?)<.*?fraction.*?>(.*?)<', re.S)

    url_dic = {
        'http://maoyan.com/board/7': pattern1,
    }

    pool = Pool(processes=3)
    res_l = []
    for url, pattern in url_dic.items():
        ##  回调函数存在与否的区别
        # res = p.apply_async(get_page, args=(url, pattern), callback=parse_pageparse_page)
        # res = pool.apply_async(get_page, args=(url, pattern))

        ## 同步与异步的区别
        res = pool.apply_async(get_page, args=(url, pattern))
        # res = pool.apply(get_page, args=(url, pattern))
        res_l.append(res)

    for res in res_l:
        res.get()


def manage_write(queue):
    print('manage write start.')
    for ch in 'DONGGE':
        queue.put(ch)


def manage_read(queue):
    print('manage read start')
    while 1:
        if queue.empty():
            break
        else:
            print u'read get from queue：', queue.get()


def manage_pool_run():
    print 'main process(%s) start' % os.getpid()

    queue = Manager().Queue()  # Manager中的Queue才能配合Pool
    pool = Pool(processes=3)

    # 同步与异步的区别
    pool.apply(manage_write, args=(queue,))
    pool.apply(manage_read, args=(queue,))

    pool.apply_async(manage_write, args=(queue,))
    pool.apply_async(manage_read, args=(queue,))

    pool.close()  # 不允许进程池再加新的请求了
    pool.join()

    print 'main process(%s) end' % os.getpid()


def job(x):
    return x * x


def multicore():
    pool = Pool(processes=2)
    res = pool.map(job, range(10))
    print(res)
    res = pool.apply_async(job, (2,))
    print(res.get())
    multi_res = [pool.apply_async(job, (i,)) for i in range(10)]
    print([res.get() for res in multi_res])


def job_lock(v, num, l):
    l.acquire()
    for _ in range(10):
        time.sleep(0.1)
        v.value += num
        print(v.value)
    l.release()


def multi_process():
    l = Lock()
    v = Value('i', 0)
    p1 = Process(target=job_lock, args=(v, 1, l))
    p2 = Process(target=job_lock, args=(v, 3, l))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    # run()
    # multiprocess_run()
    # mutilpriocess_pool_run()
    manage_pool_run()
    # multicore()
    # multi_process()
