#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import Binarizer
import numpy as np

data_set = pd.read_csv('pima-indians-diabetes.csv')
# print(data_set)

# define feature columns which will be selected for analysis
feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
X = data_set[feature_columns]  # get feature column
y = data_set.label  # get label

# print(X)
# print(y)

##
prep_minmax = MinMaxScaler()
X_trans = prep_minmax.fit_transform(X)
# print(X_trans)  # original output
np.set_printoptions(precision=3)
print(X_trans)  # format the original output


##
prep_standard = StandardScaler()
X_trans = prep_standard.fit_transform(X)
# print(X_trans)
np.set_printoptions(precision=3)
print(X_trans)

##
prep_norm = Normalizer()
X_trans = prep_norm.fit_transform(X)
# print(X_trans)
np.set_printoptions(precision=3)
print(X_trans)

##
prep_bin = Binarizer()
X_trans = prep_bin.fit_transform(X)
# print(X_trans)
np.set_printoptions(precision=3)
print(X_trans)
