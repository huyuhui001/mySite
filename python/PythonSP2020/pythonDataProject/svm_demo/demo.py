#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

data_set = pd.read_csv('letter-recognition.csv')

feature_columns = data_set.columns[1:]
X = data_set[feature_columns]
y = data_set.lettr

print('===data_set===')
print(data_set)
print('===feature_columns===')
print(feature_columns)
print('===X===')
print(X)
print('===y===')
print(y)
print('===X, y===')
print(X, y)

svc = SVC()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)

print('===accuracy score===')
print(accuracy_score(y_test, y_pred))
print('===confusion_matrix===')
print(confusion_matrix(y_test, y_pred))