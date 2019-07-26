#!/usr/bin/python
# coding=utf8
import numpy as np
import tensorflow as tf

__author__ = 'Jam'
__date__ = '2019/7/3 14:46'

arr = np.zeros(10).reshape(2, 5)
print(arr)
print('broadcast1'.center(50,'-'))

arr = np.arange(5)
arr = arr * 4
print(arr)
print('broadcast2'.center(50,'-'))

arr = np.arange(12).reshape(4, 3)
print(arr)
print(arr.mean(axis=1))
print(arr.mean(axis=1).reshape(4,1))
print(arr - arr.mean(axis=0))
print('broadcast3'.center(50,'-'))

arr = np.arange(12).reshape(4, 3)
print(arr)
arr = arr-arr.mean(1).reshape((4,1))
print(arr.mean(1))
print(arr.mean(1).reshape((4,1)))
print(arr)
print('broadcast4'.center(50,'-'))


arr2 = np.arange(24).reshape((2,3,4))
arr3_0 = np.arange(12).reshape((3,4))

print("0轴广播")
print(arr2)
print(arr3_0)
print(arr2 - arr3_0)

arr3_1 = np.arange(8).reshape((2,1,4))
print("1轴广播")
print(arr2)
print(arr3_1)
print(arr2 - arr3_1)

arr3_2 = np.arange(6).reshape((2,3,1))
print("2轴广播")
print(arr2)
print(arr3_2)
print(arr2 - arr3_2)

print('tensorflow1'.center(50,'-'))
sess = tf.Session()
hello = tf.constant(u'Hello, TensorFlow!')
print(sess.run(hello))

print('tensorflow2'.center(50,'-'))
sess = tf.Session()
a = tf.Variable(tf.random_normal((2,3),0,0.1))
print(a)
sess.run(tf.global_variables_initializer())
print(sess.run(a))

print('tensorflow3'.center(50,'-'))
sess = tf.Session()
a = tf.Variable(tf.random_normal((2,3),0,0.1))
b = tf.Variable(tf.random_normal((2,1),0,0.1))
print(a)
print(b)
c = a - b
sess.run(tf.global_variables_initializer())
print(sess.run(c))

sess = tf.Session()
a = tf.Variable(tf.random_normal((2,3,4),0,0.1))
b = tf.Variable(tf.random_normal((2,4),0,0.1))
c = a - b
sess.run(tf.global_variables_initializer())
print(sess.run(c))