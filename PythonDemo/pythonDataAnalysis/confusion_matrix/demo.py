#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# It's to practice on how to evaluate accuracy score of different classification models
# sklearn.metrics.confusion_matrix:
#    *)Compute confusion matrix to evaluate the accuracy of a classification.
# sklearn.metrics.accuracy_score:
#     *)Accuracy classification score.
#     *)In multilabel classification, this function computes subset accuracy:
#       the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true.

from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

X, y, = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

# # Use SVC model
# svm = SVC()
# svm.fit(X_train, y_train)
# y_pred = svm.predict(X_test)

# Use KNN model
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# # Use DTC model
# dtc = DecisionTreeClassifier()
# dtc.fit(X_train, y_train)
# y_pred = dtc.predict(X_test)

print(accuracy_score(y_test, y_pred))
print(y_test)
print(y_pred)
print(confusion_matrix(y_test, y_pred))

# Use SVC model
# 0.9473684210526315
# [2 1 0 0 0 2 1 0 0 1 1 0 2 1 1 0 2 2 0 2 1 0 2 1 0 0 2 0 2 2 2 0 0 1 0 2 1 0]
# [2 1 0 0 0 2 1 0 0 1 1 0 2 1 1 0 2 2 0 2 1 0 2 1 0 0 2 0 2 1 2 0 0 1 0 1 1 0]
# [[16  0  0]
#  [ 0 10  0]
#  [ 0  2 10]]
#


# Use KNN model
# 0.9736842105263158
# [1 1 2 2 0 0 1 0 1 2 0 1 1 0 1 0 2 1 0 1 2 1 1 2 0 2 2 1 0 0 1 0 0 0 1 1 0 1]
# [1 1 2 2 0 0 1 0 1 2 0 1 1 0 1 0 2 1 0 1 2 1 1 2 0 2 2 1 0 0 1 0 0 0 1 1 0 2]
# [[14  0  0]
#  [ 0 15  1]
#  [ 0  0  8]]


# Use DTC model
# 0.9210526315789473
# [1 1 2 1 1 1 0 0 0 2 0 0 0 1 0 2 1 1 0 1 0 0 0 1 0 2 1 1 0 2 2 2 1 0 1 1 2 1]
# [1 1 2 1 2 1 0 0 0 2 0 0 0 1 0 2 1 1 0 1 0 0 0 1 0 2 1 2 0 2 1 2 1 0 1 1 2 1]
# [[14  0  0]
#  [ 0 14  2]
#  [ 0  1  7]]
