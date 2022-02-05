#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# This is to get an overall understanding of different modeling for classification


from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold  # 均匀分布数据样本和标签，避免某个样本集的标签是完全一样的情况
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import numpy as np

""" ====== Load data set ======
Load and return the iris dataset (classification).
"""
X, y = load_iris(return_X_y=True)

""" ====== Define a list for different modeling for classification 数据分类 ======
sklearn.neighbors.KNeighborsClassifier
    *)Classifier implementing the k-nearest neighbors vote. 实现了K最近邻居投票算法的分类器

sklearn.tree.DecisionTreeClassifier
    *)A decision tree classifier. 构建决策树，默认使用CART算法。基尼系数是CART算法中采用的度量标准
    *)决策树是一种树形结构，其中每个内部节点表示一个属性上的测试，每个分支代表一个测试输出，每个叶节点代表一种类别。

sklearn.naive_bayes.GaussianNB
    *)GaussianNB implements the Gaussian Naive Bayes algorithm for classification 朴素贝叶斯分类器
    *)一共有3个朴素贝叶斯的分类算法类。分别是GaussianNB，MultinomialNB和BernoulliNB
        *)GaussianNB就是先验为高斯分布的朴素贝叶斯，适用于样本特征的分布大部分是连续值
        *)MultinomialNB就是先验为多项式分布的朴素贝叶斯，适用于样本特征的分布大部分是多元离散值
        *)BernoulliNB就是先验为伯努利分布的朴素贝叶斯，适用于样本特征是二元离散值或者很稀疏的多元离散值

sklearn.svm.SVC
    *)C-Support Vector Classification.
"""
models = []
models.append(('KNN', KNeighborsClassifier()))
models.append(('DTC', DecisionTreeClassifier()))
models.append(('GNB', GaussianNB()))
models.append(('SVM', SVC()))

print("------print models------")
print(models)
# [('KNN', KNeighborsClassifier()), ('DTC', DecisionTreeClassifier()), ('GNB', GaussianNB()), ('SVM', SVC())]

result_set = []
names = []

for name, model in models:
    # Provides train/test indices to split data in train/test sets.
    # 均匀分布数据样本和标签，避免某个样本集的标签是完全一样的情况，不指定则n_splits默认为5
    skf = StratifiedKFold(n_splits=10)

    # sklearn.model_selection.cross_val_score is to evaluate a score by cross-validation
    cv_score = cross_val_score(model, X, y, cv=skf, scoring='accuracy')
    result_set.append((cv_score))
    names.append(name)  # model names

    np.set_printoptions(precision=3)  # 控制输出的小数点个数为3，默认是8
    print("------print cv_score------")
    print(cv_score)

    # Compare mean value, standard deviation, and variance of each classification model
    # mean: mean value 均值 ，越高越好
    # var: variance 方差， 越小越好
    # std: standard deviation 标准差
    print("------print evaluation of each classification model------")
    print('%s: %.f  %.f  (%.f)' % (name, cv_score.mean(), cv_score.std(), cv_score.var()))

plt.boxplot(result_set, labels=names)
plt.show()  # 图形中的橙色线代表中位数，类似正态分布的峰值 https://blog.csdn.net/Arwen_H/article/details/84855825


# 不指定n_splits
# KNN: 0.973333  0.024944  (0.000622)
# DTC: 0.960000  0.032660  (0.001067)
# GNB: 0.953333  0.026667  (0.000711)
# SVM: 0.966667  0.021082  (0.000444)


# 指定n_splits=10
# [1.         0.93333333 1.         1.         0.86666667 0.93333333  0.93333333 1.         1.         1.        ]
# KNN: 0.966667  0.044721  (0.002000)
# [1.         0.93333333 1.         0.93333333 0.93333333 0.86666667  0.93333333 0.93333333 1.         1.        ]
# DTC: 0.953333  0.042687  (0.001822)
# [0.93333333 0.93333333 1.         0.93333333 0.93333333 0.93333333  0.86666667 1.         1.         1.        ]
# GNB: 0.953333  0.042687  (0.001822)
# [1.         0.93333333 1.         1.         1.         0.93333333  0.93333333 0.93333333 1.         1.        ]
# SVM: 0.973333  0.032660  (0.001067)
