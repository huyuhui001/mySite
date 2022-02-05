#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# It's to understand how to implement cluster (聚类) by KMeans
# 有三类比较常见的聚类模型，K-mean聚类、层次（系统）聚类、最大期望EM算法

from sklearn.cluster import KMeans


def load_data(path):
    file = open(path, 'r')
    lines = file.readlines()
    customer_names = []
    data_set = []
    for line in lines:
        items = line.strip().split(',')
        customer_names.append(items[0])
        data_set.append([float(items[i]) for i in range(1, len(items))])

    print("---print customer_names---")
    print(customer_names)

    print("---print data_set---")
    print(data_set)

    return customer_names, data_set


if __name__ == '__main__':
    customer_names, data_set = load_data('customer')
    # print(customer_names, data_set)

    kmeans = KMeans(n_clusters=3)  # n_clusters:簇的个数，即你想聚成几类
    labels = kmeans.fit_predict(data_set)
    print("---labels---")
    print(labels)  # Noticed that there are only 3 different labels: 0, 1, 2

    customer_cluster = [[], [], []]  # three groups: 0, 1, 2 in data set [0 0 0 0 0 0 1 2 1 0 0 2 1 2 0 0 0 1 1 0]

    for i in range(len(customer_names)):
        customer_cluster[labels[i]].append(customer_names[i])

    print("---print customer_cluster---")
    for i in range(len(customer_cluster)):
        print(customer_cluster[i])

    # 返回预测的样本属于的类的聚类中心
    print("返回预测的样本属于的类的聚类中心")
    print(kmeans.fit_predict(data_set))
    print(kmeans.predict(data_set))

    # 返回每个样本与聚类质心的距离
    print("返回每个样本与聚类质心的距离")
    print(kmeans.fit_transform(data_set))
    print(kmeans.transform(data_set))

    # 评价聚类好坏
    print("评价聚类好坏")
    print(kmeans.score(data_set))




# [1 1 1 1 1 1 0 2 0 1 1 2 0 2 1 1 1 0 0 1]
# ['customer7', 'customer9', 'customer13', 'customer18', 'customer19']
# ['customer1', 'customer2', 'customer3', 'customer4', 'customer5', 'customer6', 'customer10', 'customer11', 'customer15', 'customer16', 'customer17', 'customer20']
# ['customer8', 'customer12', 'customer14']
