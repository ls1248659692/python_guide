#!/usr/bin/python
# coding=utf8
from collections import defaultdict, OrderedDict

__author__ = 'Jam'
__date__ = '2019/5/30 15:22'


class Node(object):
    __slots__ = ('key', 'val', 'cnt')

    def __init__(self, key, val, cnt=0):
        self.key, self.val, self.cnt = key, val, cnt

    def __str__(self):
        return 'cache --> key:%s,val:%s,cnt:%s' % (self.key, self.val, self.cnt)


class LFUCache(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.cnt2node = defaultdict(OrderedDict)
        self.mincnt = 0

    def put(self, key, value):
        if key in self.cache:
            self.cache[key].val = value
            self.get(key)
            return

        if len(self.cache) >= self.capacity:
            pop_key, _pop_node = self.cnt2node[self.mincnt].popitem(last=False)
            del self.cache[pop_key]

        self.cache[key] = self.cnt2node[1][key] = Node(key, value, 1)
        self.mincnt = 1

    def get(self, key, default=-1):
        if key not in self.cache:
            return default

        node = self.cache[key]
        del self.cnt2node[node.cnt][key]

        if not self.cnt2node[node.cnt]:
            del self.cnt2node[node.cnt]

        node.cnt += 1
        self.cnt2node[node.cnt][key] = node

        if not self.cnt2node[self.mincnt]:
            self.mincnt += 1
        return node.val


def test_lfu():
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    assert c.get(3) == 3
    c.put(4, 4)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


def unit_test():
    test_lfu()


if __name__ == '__main__':
    unit_test()
