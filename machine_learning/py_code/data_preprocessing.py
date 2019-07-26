#!/usr/bin/python
# coding=utf8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

__author__ = 'Jam'
__date__ = '2019/4/26 17:10'

print("-" * 70)
print("Step 1: Importing dataset")
dataset = pd.read_csv('../datasets/Data.csv')
print('dataset \n', dataset)

X = dataset.iloc[:, :-1].values
Y = dataset.iloc[:, -1].values
print('X \n', X)
print('Y \n', Y)

print("-" * 70)
print("Step 2: Handling the missing data")
imputer = Imputer(missing_values="NaN", strategy="mean", axis=0)  # axis=0表示按列方向
imputer = imputer.fit(X[:, 1:])
X[:, 1:] = imputer.transform(X[:, 1:])
print('X \n', X)

print("-" * 70)
print("Step 3: Encoding categorical data")
labelencoder_X = LabelEncoder()
X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
print('X \n', X)

onehotencoder = OneHotEncoder(categorical_features=[0])
X = onehotencoder.fit_transform(X).toarray()
labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(Y)
print('X \n', X)
print('Y \n', Y)

print("-" * 70)
print("Step 4: Splitting the datasets into training sets and Test sets")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
print("X_train \n", X_train)
print("Y_train \n", Y_train)
print("X_test \n", X_test)
print("Y_test \n", Y_test)
