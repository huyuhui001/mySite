#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

"""====== Load data set ======
Load and return the iris dataset (classification).
The iris dataset is a classic and very easy multi-class classification dataset.

load_iris: (sklearn.datasets)
    *)If return_X_y=True, 
        the data is a pandas DataFrame including columns with appropriate dtypes (numeric). 
        the target is a pandas DataFrame or Series depending on the number of target columns. 
        then (data, target) will be pandas DataFrames or Series specified.

train_test_split: (sklearn.model_selection)
    *)Split arrays or matrices into random train and test subsets
    *)Test subset: X, y (X: Samples, y: features)
    *)Returns: list, which contains train-test split of inputs
"""
X, y, = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)  # Split data, use 25% data for test samples


"""====== Define algorithm ======
GaussianNB implements the Gaussian Naive Bayes algorithm for classification
"""
gau = GaussianNB()

"""====== Fit ======
Fit Gaussian Naive Bayes according to X, y (X: samples, y: features)
Fit和train不同的是，它并不是一个训练Train的过程，而是一个适配的过程，过程都是定死的，最后只是得到了一个统一的转换的规则模型。
"""
gau.fit(X_train, y_train)


"""====== Train data split ======
Perform classification on an array of test vectors X
"""
y_pred = gau.predict(X_test)  # Train 25% test data


"""====== Accuracy Score ======
sklearn.metrics.confusion_matrix:
    *)Compute confusion matrix to evaluate the accuracy of a classification.

sklearn.metrics.accuracy_score:
    *)Accuracy classification score.
    *)In multilabel classification, this function computes subset accuracy: 
      the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true.
"""
print(X_train)
print("---------------")
print(X_test)
print("---------------")
print(y_train)
print("---------------")
print(y_test)
print("---------------")
print(y_pred)
print("---------------")
print(accuracy_score(y_test, y_pred))
print("---------------")
print(confusion_matrix(y_test, y_pred))