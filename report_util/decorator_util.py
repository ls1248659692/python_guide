#!/usr/bin/python
# coding=utf8
import time
import traceback

__author__ = 'Jam'
__date__ = '2019/3/13 15:28'


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print('[{function}]: time used: {used_time} seconds.'.format(
            used_time=round(time.time() - start, 3),
            function=func.__name__
        ))
        return result

    return wrapper


def separatorline(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s\t\t%s' % (time.ctime(), '-' * 30))
        return result

    return wrapper


def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except:
            traceback.print_exc()

    return wrapper


def deco(*args, **kwargs):
    def _deco(func):
        def __deco():
            print("before %s called." % (func.__name__),args,kwargs)
            result = func(*args, **kwargs)
            print("after %s called." % (func.__name__),args,kwargs)
            return result
        return __deco
    return _deco


@deco("mymodule","test",test="good")
def myfunc(*args, **kwargs):
    print(" myfunc() called.")
    print(args,kwargs)


@separatorline
@timeit
def test_function():
    for num in range(1000):
        print(num)

    return 'OK'


if __name__ == "__main__":
    # print test_function()
    myfunc()