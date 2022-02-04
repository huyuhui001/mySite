#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from sklearn import datasets
from sklearn import neighbors
from sklearn import model_selection
from sklearn import metrics


class DigitalIdentify(object):
    def digit_identify(self):
        X, y = datasets.load_digits(return_X_y=True)
        print(X.shape)  # (1797, 64)  -- 1797 samples, and 64 features of each sample
        knn = neighbors.KNeighborsClassifier()
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        print(y_pred)
        print(y_test)
        pred_score = metrics.accuracy_score(y_test, y_pred)
        print(pred_score)


if __name__ == '__main__':
    di = DigitalIdentify()
    di.digit_identify()
