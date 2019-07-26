#!/usr/bin/python
# coding=utf8
import itertools

__author__ = 'Jam'
__date__ = '2018/12/14 15:56'


## one list
def product(repeat_num=2):
    print 'product 3^2'
    for i in itertools.product([1, 2, 3], repeat=repeat_num):
        print(i)

    print 'permutation A(3,2)'
    for i in itertools.permutations([1, 2, 3], repeat_num):
        print i

    print 'combination  C(3,2)'
    for i in itertools.combinations([1, 2, 3], repeat_num):
        print(i)

    print   'combinations_with_replacement  C(3,2)'
    for i in itertools.combinations_with_replacement([1, 2, 3], 3):
        print(i)


## two list
def product_test():
    print  '3X3X2'
    a = ['1', '2', '3']
    b = ['a', 'b', 'c']
    for r in itertools.product(a, b):
        for a, b in itertools.permutations(r, 2):
            print(a + b)

    print  '3X3'
    a = ['1']
    b = ['a', 'b', 'c']
    for r in itertools.product(a, b):
        print r


if __name__ == '__main__':
    # product()
    product_test()
