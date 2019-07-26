#!/usr/bin/python
# coding=utf8
import random

__author__ = 'Jam'
__date__ = '2019/5/18 12:36'


def binary_search(array, target):
    if not array:
        return -1
    beg, end = 0, len(array)
    while beg < end:
        mid = beg + (end - beg) // 2
        if array[mid] == target:
            return mid
        elif array[mid] > target:
            end = mid
        else:
            beg = mid + 1
    return -1


def linear_search(predicate, iterable):
    for index, val in enumerate(iterable):
        if predicate(val):
            return index
    return -1


def merge_sort(seq):
    if len(seq) <= 1:
        return seq
    else:
        mid = int(len(seq) / 2)
        left_half = merge_sort(seq[:mid])
        right_half = merge_sort(seq[mid:])

        new_seq = merge_sorted_list(left_half, right_half)
        return new_seq


def merge_sorted_list(sorted_a, sorted_b):
    length_a, length_b = len(sorted_a), len(sorted_b)
    a = b = 0
    new_sorted_seq = list()

    while a < length_a and b < length_b:
        if sorted_a[a] < sorted_b[b]:
            new_sorted_seq.append(sorted_a[a])
            a += 1
        else:
            new_sorted_seq.append(sorted_b[b])
            b += 1

    if a < length_a:
        new_sorted_seq.extend(sorted_a[a:])
    else:
        new_sorted_seq.extend(sorted_b[b:])

    return new_sorted_seq


def test():
    """
    如何设计测试用例：
    - 正常值功能测试
    - 边界值（比如最大最小，最左最右值）
    - 异常值（比如 None，空值，非法值）
    """
    # 正常值，包含有和无两种结果
    number_list = [0, 1, 2, 3, 4, 5]
    assert binary_search(number_list, 1) == 1
    assert binary_search(number_list, 6) == -1
    assert binary_search(number_list, -1) == -1
    # 边界值
    assert binary_search(number_list, 0) == 0
    assert binary_search(number_list, 5) == 5
    assert binary_search([0], 0) == 0
    # 异常值
    assert binary_search([], 1) == -1

    assert linear_search(lambda x: x == 5, number_list) == 5

    random.shuffle(number_list)
    assert merge_sort(number_list) == sorted(number_list)


if __name__ == '__main__':
    test()
