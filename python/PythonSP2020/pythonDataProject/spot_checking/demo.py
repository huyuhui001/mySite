#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import Binarizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import numpy as np

data_set = pd.read_csv('pima-indians-diabetes.csv')
# print(data_set)

# define feature columns which will be selected for analysis
feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
X = data_set[feature_columns]  # get feature column
y = data_set.label  # get label

# Clean data
prep = MinMaxScaler()
# prep = StandardScaler()
# prep = Normalizer()
# prep = Binarizer()
X_trans = prep.fit_transform(X)

# Preprocess data with 10 times KFold
kfold = KFold(n_splits=10)  # 10 times KFold
mode = LogisticRegression()
cv_score = cross_val_score(mode, X_trans, y, cv=kfold)
print("cv score: ", cv_score)
print('mean: %.2f std: %2f var: %.2f' % (cv_score(), cv_score.std(), cv_score.var()))








# MinMaxScaler
# KFold = 10: [0.6 0.4 0.6 0.6 0.8 0.8 0.7 0.8 0.8 0.7]
# StandardScaler
# KFold = 10: [0.6 0.5 0.7 0.5 0.5 0.7 0.7 0.8 0.8 0.8]
# Normalizer
# KFold = 10: [0.4 0.3 0.5 0.6 0.7 0.8 0.7 0.7 0.8 0.8]
# Binarizer
# KFold = 10: [0.4 0.3 0.5 0.6 0.7 0.5 0.7 0.7 0.7 0.8]




# ***********************************
# Error: STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.. Data quality is not good. Need preprocessing data.



