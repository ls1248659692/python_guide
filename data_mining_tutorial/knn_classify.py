#!/usr/bin/python
# coding=utf8
import csv
import os
from collections import defaultdict

import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

__author__ = 'Jam'
__date__ = '2019/6/10 10:36'


def knn_classify():
    current_folder = "."
    data_folder = os.path.join(current_folder, "data")
    data_filename = os.path.join(data_folder, "ionosphere.data")

    X = np.zeros((351, 34), dtype='float')
    y = np.zeros((351,), dtype='bool')

    with open(data_filename, 'r') as input_file:
        reader = csv.reader(input_file)
        for i, row in enumerate(reader):
            data = [float(datum) for datum in row[:-1]]
            X[i] = data
            y[i] = row[-1] == 'g'  # 相当于 y[i]=1 if row[-1]=='g' else y[i]=0

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=14)
    print("训练集数据有 {} 条".format(X_train.shape[0]))
    print("测试集数据有 {} 条".format(X_test.shape[0]))
    print("每条数据有 {} 个features".format(X_train.shape[1]))

    estimator = KNeighborsClassifier()
    estimator.fit(X_train, y_train)
    y_predicted = estimator.predict(X_test)
    accuracy = np.mean(y_test == y_predicted) * 100
    print("准确率 {0:.2f}%".format(accuracy))

    scores = cross_val_score(estimator, X, y, scoring='accuracy')
    average_accuracy = np.mean(scores) * 100
    print("平均准确率 {0:.2f}%".format(average_accuracy))

    avg_scores = []
    all_scores = []
    parameter_values = list(range(1, 21))  # K通常是不大于20的整数
    for n_neighbors in parameter_values:
        estimator = KNeighborsClassifier(n_neighbors=n_neighbors)
        scores = cross_val_score(estimator, X, y, scoring='accuracy')
        avg_scores.append(np.mean(scores))
        all_scores.append(scores)

    plt.figure(figsize=(32, 20))
    plt.plot(parameter_values, avg_scores, '-o', linewidth=5, markersize=24)
    plt.plot(parameter_values, all_scores, '-x', linewidth=5, markersize=24)
    plt.axis([0, max(parameter_values), 0.6, 1.0])
    plt.show()

    for parameter, scores in zip(parameter_values, all_scores):
        n_scores = len(scores)
        plt.plot([parameter] * n_scores, scores, '-o')
    plt.show()

    plt.plot(parameter_values, all_scores, '-o')
    plt.show()

    all_scores = defaultdict(list)
    for n_neighbors in parameter_values:
        estimator = KNeighborsClassifier(n_neighbors=n_neighbors)
        scores = cross_val_score(estimator, X, y, scoring='accuracy', cv=10)
        all_scores[n_neighbors].append(scores)

    for parameter in parameter_values:
        scores = all_scores[parameter]
        n_scores = len(scores)
        plt.plot([parameter] * n_scores, scores, '-o')

    plt.show()

    plt.plot(parameter_values, avg_scores, '-o')
    plt.show()


def main():
    knn_classify()


if __name__ == '__main__':
    main()
