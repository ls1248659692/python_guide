#!/usr/bin/python
# coding=utf8

import numpy as np
from scipy import linalg

__author__ = 'Jam'
__date__ = '2019/7/17 13:29'

print("-" * 70)
a = np.array([[3, 2, 0], [1, -1, 0], [0, 5, 1]])
b = np.array([2, 4, -2])
res1 = linalg.solve(a, b)
print(res1)

print("-" * 70)
A = np.array([[1, 2], [3, 4]])
res2 = linalg.det(A)
print (res2)

print("-" * 70)
A = np.array([[1, 2], [3, 4]])
l, v = linalg.eig(A)
print(l, v)

print("-" * 70)
a = np.random.randn(2, 3) + 1.j * np.random.randn(2, 3)
U, s, Vh = linalg.svd(a)
print (U, Vh, s)
