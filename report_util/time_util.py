#!/usr/bin/python
# coding=utf8
import time

__author__ = 'Jam'
__date__ = '2018/12/28 9:54'


def timeit(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print '[{function}]: time used: {used_time} seconds.'.format(
            used_time=round(end - start, 3),
            function=func.__name__
        )
        return result

    return wrapper

@timeit
def test_function():
    for num in range(1000):
        print  num

    return 'OK'


if __name__ == "__main__":
    # timeit(test_function)()
    print test_function()
