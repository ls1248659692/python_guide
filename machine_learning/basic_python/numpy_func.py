#!/usr/bin/python
# coding=utf8
import numpy as np

__author__ = 'Jam'
__date__ = '2019/7/4 16:59'

print('*1*'.center(50, '-'))
a = np.array([1, 2, 3])
b = np.array([2, 3, 4])
print(np.stack([a, b], axis=0))
print(np.stack([a, b], axis=1))

print('*2*'.center(50, '-'))
a = np.array([[1, 2, 3]])
b = np.array([[2, 3, 4]])
print(np.stack([a, b], axis=0))

print('*3*'.center(50, '-'))
a = np.array([1, 2, 3])
b = np.array([2, 3, 4])

a = a[np.newaxis, :]
b = b[np.newaxis, :]
print(np.concatenate([a, b], axis=0))

print('*4*'.center(50, '-'))
a = np.array([1, 2, 3])
b = np.array([2, 3, 4])
print(np.hstack([a, b]))
print(np.concatenate([a, b], axis=0))

print('*5*'.center(50, '-'))
a = [[1], [2], [3]]
b = [[1], [2], [3]]
print(np.hstack([a, b]))
print(np.concatenate([a, b], axis=1))

print('*6*'.center(50, '-'))
a = [[[1]], [[2]], [[3]]]
b = [[[2]], [[3]], [[4]]]
print(np.hstack([a, b]))
print(np.concatenate([a, b], axis=1))

print('*7*'.center(50, '-'))
a = np.array([1, 2, 3])
b = np.array([2, 3, 4])
print(np.vstack([a, b]))
np.concatenate([a, b], axis=0)

print('*8*'.center(50, '-'))
a = [[1], [2], [3]]
b = [[1], [2], [3]]
print(np.vstack([a, b]))
print(np.concatenate([a, b], axis=0))

print('*9*'.center(50, '-'))
a = [[[1]], [[2]], [[3]]]
b = [[[2]], [[3]], [[4]]]
print(np.vstack([a, b]))
print(np.concatenate([a, b], axis=0))

print('*10*'.center(50, '-'))
