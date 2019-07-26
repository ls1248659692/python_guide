#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/5/29 14:24'


def flatten(rec_list):
    for i in rec_list:
        if isinstance(i, list):
            for i in flatten(i):
                yield i
        else:
            yield i


def test_flatten():
    print list(flatten([]))
    assert list(flatten([])) == []
    print list(flatten([[[1, [1, [1, 1, [1]]]], 2, 3], [1, 2, 3]]))
    assert list(flatten([[[1, [1, [1, 1, [1]]]], 2, 3], [1, 2, 3]])) == [1, 1, 1, 1, 1, 2, 3, 1, 2, 3]


if __name__ == '__main__':
    test_flatten()
