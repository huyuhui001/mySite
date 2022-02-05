#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from sklearn import datasets
from sklearn import neighbors  # use KNN
import numpy as np
import matplotlib.pyplot as plt


class DigitalIdentify(object):
    def digit_identify(self):
        X, y = datasets.load_digits(return_X_y=True)
        # print(X, y)
        knn = neighbors.KNeighborsClassifier()
        knn.fit(X, y)
        print(X, y)

        '''
        data_set = datasets.load_digits()
        knn = neighbors.KNeighborsClassifier()

        knn.fit(data_set.data, data_set.target)  # learn, adopt. X means data, y means label
        print(data_set.data.shape, data_set.data, data_set.target)
        # print(data_set.data[5], data_set.target[8])
        '''

        test_data = [0, 0, 9, 14, 8, 1, 0, 0,
                     0, 0, 12, 14, 14, 12, 0, 0,
                     0, 0, 9, 10, 0, 15, 4, 0,
                     0, 0, 3, 16, 12, 14, 2, 0,
                     0, 0, 4, 16, 16, 2, 0, 0,
                     0, 3, 16, 8, 10, 13, 2, 0,
                     0, 1, 15, 1, 3, 16, 8, 0,
                     0, 0, 11, 16, 15, 11, 1, 0]

        predict_result = knn.predict(np.array(test_data).reshape(1, -1))
        print(predict_result)


if __name__ == '__main__':
    di = DigitalIdentify()
    di.digit_identify()

'''
data_set = datasets.load_digits()

print(data_set)
print(data_set.data[0])  # a list
print(data_set.images[0])  # 8x8 array
plt.matshow(data_set.images[5])
plt.show()

'''
