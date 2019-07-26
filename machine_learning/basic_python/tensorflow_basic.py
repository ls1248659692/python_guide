#!/usr/bin/python
# coding=utf8

import numpy as np
import tensorflow as tf

__author__ = 'Jam'
__date__ = '2019/7/5 10:40'

row_dim = col_dim = 5

zero_tsr = tf.zeros([row_dim, col_dim])
ones_tsr = tf.ones([row_dim, col_dim])
filled_tsr = tf.fill([row_dim, col_dim], 42)

constant_tsr1 = tf.constant([1, 2, 3])
zeros_similar = tf.zeros_like(constant_tsr1)
ones_similar = tf.ones_like(constant_tsr1)

linear_tsr = tf.linspace(start=0., stop=1., num=3)
inter_seq_tsr = tf.range(start=6, limit=16, delta=3)

rand_unif_tsr = tf.random_uniform([row_dim, col_dim], minval=0, maxval=1)
rand_norm_tsr = tf.random_normal([row_dim, col_dim], mean=0.0, stddev=1.0)
trunc_norm_tsr = tf.truncated_normal([row_dim, col_dim], mean=0.0, stddev=1.0)

my_var = tf.convert_to_tensor([1, 2, 3])
initialize_op = tf.global_variables_initializer()

x = tf.placeholder(shape=[2, 2], dtype=tf.float32)
y = tf.identity(x)
x_vals = np.random.rand(2, 2)

first_var = tf.Variable(tf.zeros([2, 3]))
second_var = tf.Variable(tf.zeros_like(first_var))

identity_matrix = tf.diag([1., 1., 1.])
A = tf.truncated_normal([2, 3])
B = tf.fill([2, 3], 5.0)
C = tf.random_uniform([3, 2])
D = tf.convert_to_tensor(np.array([[1., 2., 3.],
                                   [-3., -7., -1.],
                                   [0., 5., -2.]]))

input1 = tf.placeholder(dtype=tf.float32)
input2 = tf.placeholder(dtype=tf.float32)

output = tf.multiply(input1, input2)

with tf.Session() as sess:
    print('*1*'.center(50, '-'))
    print(sess.run(zero_tsr))
    print(sess.run(ones_tsr))
    print(sess.run(filled_tsr))
    print('*2*'.center(50, '-'))
    print(sess.run(constant_tsr1))
    print(sess.run(zeros_similar))
    print(sess.run(ones_similar))
    print('*3*'.center(50, '-'))
    print(sess.run(linear_tsr))
    print(sess.run(inter_seq_tsr))
    print('*4*'.center(50, '-'))
    print(sess.run(rand_unif_tsr))
    print(sess.run(rand_norm_tsr))
    print(sess.run(trunc_norm_tsr))
    print('*5*'.center(50, '-'))
    print(sess.run(my_var))
    print('*6*'.center(50, '-'))
    print(x_vals)
    print(sess.run(y, feed_dict={x: x_vals}))
    print('*7*'.center(50, '-'))
    print(sess.run(first_var.initializer))
    print(sess.run(second_var.initializer))
    print('*8*'.center(50, '-'))
    # print(sess.run(identity_matrix))
    print(sess.run(A))
    print(sess.run(B))
    print(sess.run(C))
    print(sess.run(D))
    print('*9*'.center(50, '-'))
    print(sess.run(A))
    print(sess.run(A + B))
    print(sess.run(tf.add(A, B)))
    print(sess.run(A - B))
    print(sess.run(tf.subtract(A, B)))
    print(sess.run(tf.matmul(B, identity_matrix)))
    print(sess.run(tf.transpose(C)))
    print(sess.run(tf.matrix_determinant(D)))
    print(sess.run(tf.matrix_inverse(D)))
    print(sess.run(tf.cholesky(identity_matrix)))
    print(sess.run(tf.self_adjoint_eig(D)))
    print('*10*'.center(50, '-'))
    # print(sess.run(tf.div(3,4)))
    print(sess.run(tf.truediv(3, 4)))
    print(sess.run(tf.floordiv(3.0, 4.0)))
    print(sess.run(tf.mod(22.0, 5.0)))
    print(sess.run(tf.cross([1., 0., 0.], [0., 1., 0.])))
    print('*12*'.center(50, '-'))
    print(sess.run(output, feed_dict={input1: [3.], input2: [5]}))

"""
TensorFlow是采用数据流图（data　flow　graphs）来计算, 所以首先我们得创建一个数据流流图,
然后再将我们的数据（数据以张量(tensor)的形式存在）放在数据流图中计算. 节点（Nodes）在图
中表示数学操作,图中的线（edges）则表示在节点间相互联系的多维数据数组, 即张量（tensor).
训练模型时tensor会不断的从数据流图中的一个节点flow到另一节点, 这就是TensorFlow名字的由来.
  
Tensor 张量意义

张量（Tensor):

张量有多种. 零阶张量为 纯量或标量 (scalar) 也就是一个数值. 比如 [1]
一阶张量为 向量 (vector), 比如 一维的 [1, 2, 3]
二阶张量为 矩阵 (matrix), 比如 二维的 [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
以此类推, 还有 三阶 三维的

"""

x_data = np.random.rand(100).astype(np.float32)
y_data = x_data * 0.1 + 0.3

Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
biases = tf.Variable(tf.zeros([1]))

y = Weights * x_data + biases
loss = tf.reduce_mean(tf.square(y - y_data))

optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

for step in range(201):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))

print('*13*'.center(50, '-'))
