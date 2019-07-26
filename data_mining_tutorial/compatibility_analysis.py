#!/usr/bin/python
# coding=utf8

from collections import defaultdict
from operator import itemgetter
from pprint import pprint

from sklearn.datasets import load_iris
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

__author__ = 'Jam'
__date__ = '2019/6/6 14:54'

import numpy as np

"""
亲和性分析
如果一个顾客买了商品X，那么他们可能愿意买商品Y
衡量方法：

支持度support := 所有买X的人数

置信度confidence :=  所有买𝑋和𝑌的人数/所有买𝑋的人数
"""


def crate_random_data():
    X = np.zeros((100, 5), dtype='bool')

    for i in range(X.shape[0]):
        if np.random.random() < 0.3:
            X[i][0] = 1
            if np.random.random() < 0.5:
                X[i][1] = 1
            if np.random.random() < 0.2:
                X[i][2] = 1
            if np.random.random() < 0.25:
                X[i][3] = 1
            if np.random.random() < 0.5:
                X[i][4] = 1
        else:
            if np.random.random() < 0.5:
                X[i][1] = 1
                if np.random.random() < 0.2:
                    X[i][2] = 1
                if np.random.random() < 0.25:
                    X[i][3] = 1
                if np.random.random() < 0.5:
                    X[i][4] = 1
            else:
                if np.random.random() < 0.8:
                    X[i][2] = 1
                if np.random.random() < 0.6:
                    X[i][3] = 1
                if np.random.random() < 0.7:
                    X[i][4] = 1

        if X[i].sum() == 0:
            X[i][4] = 1
    np.savetxt("./data/affinity_dataset.txt", X, fmt='%d')  # 保存


def print_rule(premise, conclusion, support, confidence, features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    print("Rule: 买了{0}，又买{1}".format(premise_name, conclusion_name))
    print(" - 置信度Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
    print(" - 支持度Support: {0}".format(support[(premise, conclusion)]))
    print("")


def special_condiction():
    dataset_filename = "./data/affinity_dataset.txt"
    X = np.loadtxt(dataset_filename)  # 加载数据
    # features = ["bread", "milk", "cheese", "apples", "bananas"]

    num_apple_purchases = 0  # 计数
    for sample in X:
        if sample[3] == 1:  # 记录买 Apples　的有多少人
            num_apple_purchases += 1
    print("买苹果的有{0}人".format(num_apple_purchases))

    rule_valid = 0
    rule_invalid = 0
    for sample in X:
        if sample[3] == 1:  # 买了苹果
            if sample[4] == 1:  # 又买香蕉的
                rule_valid += 1
            else:  # 不买香蕉的
                rule_invalid += 1
    print("买了苹果又买香蕉的有{0}人".format(rule_valid))
    print("买了苹果不买香蕉的有{0}人".format(rule_invalid))

    support = rule_valid
    confidence = rule_valid * 1.0 / num_apple_purchases
    print("支持度support = {0} 置信度confidence = {1:.3f}.".format(support, confidence))
    print("置信度confidence的百分比形式为 {0:.1f}%.".format(100 * confidence))


def every_condiction():
    dataset_filename = "./data/affinity_dataset.txt"
    X = np.loadtxt(dataset_filename)
    n_samples, n_features = X.shape

    features = ["bread", "milk", "cheese", "apples", "bananas"]
    valid_rules = defaultdict(int)
    invalid_rules = defaultdict(int)
    num_occurences = defaultdict(int)

    for sample in X:
        for premise in range(n_features):
            if sample[premise] == 0: continue

            num_occurences[premise] += 1
            for conclusion in range(n_features):
                if premise == conclusion:
                    continue
                if sample[conclusion] == 1:
                    valid_rules[(premise, conclusion)] += 1
                else:
                    invalid_rules[(premise, conclusion)] += 1

    support = valid_rules
    confidence = defaultdict(float)
    for premise, conclusion in valid_rules.keys():
        confidence[(premise, conclusion)] = valid_rules[(premise, conclusion)] * 1.0 / num_occurences[premise]

    pprint(list(support.items()))
    pprint(list(confidence.items()))

    sorted_confidence = sorted(confidence.items(), key=itemgetter(1), reverse=True)
    pprint(sorted_confidence)

    for index in range(5):
        print("Rule #{0}".format(index + 1))
        premise, conclusion = sorted_confidence[index][0]
        print_rule(premise, conclusion, support, confidence, features)


"""
给出某一植物部分特征，预测该植物是什么
特征：

萼片长宽sepal width, sepal height
花瓣长宽petal width, petal height
算法：
 
For each variable
For each value of the variable
The prediction based on this variable goes the most frequent class
Compute the error of this prediction
Sum the prediction errors for all values of the variable
Use the variable with the lowest error
"""


def analysis_iris_data():
    dataset = load_iris()
    X = dataset.data
    y = dataset.target
    n_samples, n_features = X.shape
    print n_samples, n_features

    attribute_means = X.mean(axis=0)
    assert attribute_means.shape == (n_features,)
    X_d = np.array(X >= attribute_means, dtype='int')

    random_state = 14
    X_train, X_test, y_train, y_test = train_test_split(X_d, y, random_state=random_state)
    print("训练集数据有 {} 条".format(y_train.shape))
    print("测试集数据有 {} 条".format(y_test.shape))

    all_predictors = {variable: train(X_train, y_train, variable) for variable in range(X_train.shape[1])}
    errors = {variable: error for variable, (mapping, error) in all_predictors.items()}

    best_variable, best_error = sorted(errors.items(), key=itemgetter(1))[0]
    print("The best model is based on variable {0} and has error {1:.2f}".format(best_variable, best_error))

    model = {
        'variable': best_variable,
        'predictor': all_predictors[best_variable][0]
    }
    print(model)

    y_predicted = predict(X_test, model)
    print(y_predicted)
    accuracy = np.mean(y_predicted == y_test) * 100
    print("在测试集上的准确率 {:.1f}%".format(accuracy))
    print(classification_report(y_test, y_predicted))


def train(X, y_true, feature):
    n_samples, n_features = X.shape
    assert 0 <= feature < n_features
    values = set(X[:, feature])
    predictors = dict()
    errors = []

    for current_value in values:
        most_frequent_class, error = train_feature_value(X, y_true, feature, current_value)
        predictors[current_value] = most_frequent_class
        errors.append(error)

    total_error = sum(errors)

    return predictors, total_error


# Compute what our predictors say each sample is based on its value
# y_predicted = np.array([predictors[sample[feature]] for sample in X])

def train_feature_value(X, y_true, feature, value):
    class_counts = defaultdict(int)
    for sample, y in zip(X, y_true):
        if sample[feature] == value:
            class_counts[y] += 1

    sorted_class_counts = sorted(class_counts.items(), key=itemgetter(1), reverse=True)
    most_frequent_class = sorted_class_counts[0][0]

    n_samples = X.shape[1]
    error = sum([class_count for class_value, class_count in class_counts.items()
                 if class_value != most_frequent_class])

    return most_frequent_class, error


def predict(X_test, model):
    variable = model['variable']
    predictor = model['predictor']
    y_predicted = np.array([predictor[int(sample[variable])] for sample in X_test])
    return y_predicted


def main():
    analysis_iris_data()


if __name__ == '__main__':
    main()
