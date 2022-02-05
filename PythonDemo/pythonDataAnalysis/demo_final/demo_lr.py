#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np

data_set = pd.read_csv('pima-indians-diabetes.csv')
feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
X = data_set[feature_columns]
y = data_set.label

# model = LogisticRegression(solver='liblinear')
# model.fit(X, y)

filename = 'finalized_model.ml'

# pickle.dump(model, open(filename, 'wb'))

test_data = [1,115,70,30,96,34.6,0.529,32]
loaded_model = pickle.load(open(filename, 'rb'))
y_pred = loaded_model.predict(np.array(test_data).reshape(1, -1))
print(y_pred)












