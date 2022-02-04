#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# each row is a sample
# each column in a row is a feature
# the meaning of sample is called label or target

import numpy as np

data_set = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # samples

print(data_set)
'''
[[1 2 3]
 [4 5 6]
 [7 8 9]]
'''
print(data_set[1][1])  # 5 -- row#, column#
print(data_set[:, 1])  # [2 5 8]   column# 1
print(data_set[1, :])  # [4 5 6]   row# 1
print(data_set.reshape(1, 9))  # [[1 2 3 4 5 6 7 8 9]]  -- single sample, 9 features (multiple features)
print(data_set.reshape(1, -1))  # [[1 2 3 4 5 6 7 8 9]]
print(data_set.reshape(-1, 1))  # 9 samples (multiple), single feature
'''
[[1]
 [2]
 [3]
 [4]
 [5]
 [6]
 [7]
 [8]
 [9]]
'''
