#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
工作任务
(1)下载航空公司客户价值数据 (http://127.0.0.1:81/03/customer.txt)至Python工作文件夹；
(2)要求应用聚类分析方法，对客户进行分群；
(3)输入结果如下图所示：
Expenses.-0.14
['customer7', 'customer9', 'customer13', 'customer18', 'customer19']
Expenses.0.73
['customer1', 'customer2', 'customer3', 'customer4', 'customer5', 'customer6', 'customer10', 'customer11', 'customer15', 'customer16', 'customer17', 'customer20']
Expenses.3.11
['customer8', 'customer12', 'customer14']
"""

import numpy as np
from sklearn.cluster import KMeans


def loadData(filePath):
    fr = open(filePath, 'r+')
    lines = fr.readlines()
    retData = []
    retCustomerName = []
    for line in lines:
        items = line.strip().split(',')
        retCustomerName.append(items[0])
        retData.append([float(items[i]) for i in range(1, len(items))])
    return retData, retCustomerName


if __name__ == '__main__':
    data, CustomerName = loadData('customer.txt')
    km = KMeans(n_clusters=3)
    label = km.fit_predict(data)
    expenses = np.sum(km.cluster_centers_, axis=1)
    CustomerCluster = [[], [], []]
    for i in range(len(CustomerName)):
        CustomerCluster[label[i]].append(CustomerName[i])
    for i in range(len(CustomerCluster)):
        print("Expenses.%.2f" % expenses[i])
        print(CustomerCluster[i])
