#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from math import sqrt
from sklearn.datasets import load_iris


class KNN(object):

    def calculate_distance(self, point1, point2):
        distance = 0.0
        for i in range(len(point1)):
            if point1[i] == None:
                break
            distance += (point1[i] - point2[i]) ** 2
        return sqrt(distance)

    def find_neighbors(self, data_set, test_data):
        distances = []
        for train_data in data_set:
            distance = self.calculate_distance(test_data, train_data)
            distances.append((train_data, distance))
        distances.sort(key=lambda tup: tup[1])
        return distances[0][0]

    def predict(self, data_set, test_data):
        neighbors = self.find_neighbors(data_set, test_data)
        return neighbors[-1]

    def predict_results(self, data_set, test_data_set):
        results = []
        for test_data in test_data_set:
            y_pred = self.predict(data_set, test_data)
            results.append(y_pred)
        return results


if __name__ == '__main__':
    knn = KNN()
    X, y = load_iris(return_X_y=True)
    test_data = [4.7, 3.2, 1.3, 0.2]
    # print(X)
    print(knn.find_neighbors(X, test_data))
