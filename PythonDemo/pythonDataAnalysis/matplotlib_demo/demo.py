#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import matplotlib.pylab as plt

data_set1 = ([2, 4, 6, 8], [1, 2, 3, 4])
plt.plot(data_set1)
plt.show()

data_set2 = [0.5, 0.1, 0.3, 0.1]
data_label = ['a', 'b', 'c', 'd']
plt.pie(data_set2, labels=data_label, autopct='%.1f%%')
plt.show()

# KNN
# train data from UCI, SK_learn
