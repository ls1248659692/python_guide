#!/usr/bin/python
# coding=utf8
import heapq
import random

__author__ = 'Jam'
__date__ = '2019/5/30 16:00'


class TopK(object):
    def __init__(self, iterable, k):
        self.minheap = []
        self.capacity = k
        self.iterable = iterable

    def push(self, val):
        if len(self.minheap) >= self.capacity:
            min_val = self.minheap[0]
            if val < min_val:
                pass
            else:
                heapq.heapreplace(self.minheap, val)
        else:
            heapq.heappush(self.minheap, val)

    def get_topk(self):
        for val in self.iterable:
            self.push(val)
        return self.minheap


def test():
    number_list = list(range(1000))
    random.shuffle(number_list)

    topk = TopK(number_list, 10)
    print topk.get_topk()


if __name__ == '__main__':
    test()
