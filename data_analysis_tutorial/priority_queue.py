#!/usr/bin/python
# coding=utf8
from binary_heap import MaxHeap

__author__ = 'Jam'
__date__ = '2019/5/30 16:19'


class PriorityQueue(object):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self._maxheap = MaxHeap(maxsize)

    def push(self, priority, value):
        entry = (priority, value)
        self._maxheap.add(entry)

    def pop(self, with_priority=False):
        entry = self._maxheap.extract()
        if with_priority:
            return entry
        else:
            return entry[1]

    def is_empty(self):
        return len(self._maxheap) == 0


def test_priority_queue():
    size = 5
    pq = PriorityQueue(size)
    pq.push(5, 'purple')
    pq.push(2, 'pink')
    pq.push(0, 'white')
    pq.push(3, 'orange')
    pq.push(1, 'black')

    res = []
    with_priority = True
    while not pq.is_empty():
        res.append(pq.pop(with_priority=with_priority))

    if with_priority:
        assert res == [(5, 'purple'), (3, 'orange'), (2, 'pink'), (1, 'black'), (0, 'white')]
    else:
        assert res == ['purple', 'orange', 'pink', 'black', 'white']


if __name__ == '__main__':
    test_priority_queue()
