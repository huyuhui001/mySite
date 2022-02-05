#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


data_set = pd.read_csv('employee_data.csv')
print(data_set)
print('============')

left_emp = data_set[['satisfaction_level', 'last_evaluation']][data_set.left == 1]
# left_emp = data_set[['last_evaluation', 'time_spend_company']][data_set.left == 1]
kmeans = KMeans(n_clusters=3).fit(left_emp)

print(kmeans.labels_)
print('============')

left_emp['label'] = kmeans.labels_
print(left_emp)
print('============')

plt.scatter(left_emp['satisfaction_level'], left_emp['last_evaluation'], c=left_emp['label'])
plt.xlabel('satisfaction_level')
plt.ylabel('last_evaluation')
plt.show()


le = LabelEncoder()
data_set['Departments'] = le.fit_transform(data_set['Departments'])
data_set['salary'] = le.fit_transform(data_set['salary'])
print(data_set)
print('============')

X = data_set[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company',
              'Work_accident', 'promotion_last_5years', 'Departments', 'salary']]
y = data_set['left']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

gbc = GradientBoostingClassifier()
gbc.fit(X_train, y_train)
y_pred = gbc.predict(X_test)
print(y_pred)
print('============')
print(accuracy_score(y_test, y_pred))
print('============')


''' Demo
le = LabelEncoder()yPy
data_set['Departments'] = le.fit_transform(data_set['Departments'])
data_set['salary'] = le.fit_transform(data_set['salary'])
print(data_set)

X = data_set[['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company',
              'Work_accident', 'promotion_last_5years', 'Departments', 'salary']]
y= data_set['left']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
gbc = GradientBoostingClassifier()
gbc.fit(X_train, y_train)
y_pred = gbc.predict(X_test)
print(accuracy_score(y_test, y_pred))


'''