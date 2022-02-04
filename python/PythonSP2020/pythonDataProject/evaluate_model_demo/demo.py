#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from csv import reader
from random import randrange
from pythonDataProject.implement_algorithm_demo import KNN
import numpy as np


def load_data(path):
    data_set = []
    with open(path, 'r') as file:
        lines = reader(file)
        for line in lines:
            if not line:
                continue
            data_set.append(line)
    return data_set


def convert_to_float(data_set):
    for data in data_set:
        for i in range(len(data) - 1):
            data[i] = float(data[i].strip())


def kfold_split(data_set, n_fold):
    data_set_copy = list(data_set)
    data_set_split = list()
    fold_size = int(len(data_set) / n_fold)
    for i in range(n_fold):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(data_set_copy))
            fold.append(data_set_copy.pop(index))
        data_set_split.append(fold)
    return data_set_split


def accuracy_score(y_true, y_pred):
    correct = 0
    for i in range(len(y_true)):
        if y_true[i] == y_pred[i]:
            correct += 1
    return correct / float(len(y_true))


# Evaluate an algorithm using a cross validation split
def evaluate_algorithm(data_set, model, n_folds):
    folds = kfold_split(data_set, n_folds)
    scores = []
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        # print(train_set)
        train_set = sum(train_set, [])
        # print(train_set)
        test_set = []
        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        predicted = model.predict_results(train_set, test_set)
        actual = [row[-1] for row in fold]
        accuracy = accuracy_score(actual, predicted)
        scores.append(accuracy)
    return scores


if __name__ == '__main__':
    data_set = load_data('raw-data.csv')
    convert_to_float(data_set)
    # print(data_set)
    # print(kfold_split(data_set, n_fold=5))
    knn = KNN()
    cv_scores = evaluate_algorithm(data_set, knn, 5)
    print(cv_scores)
    print('mean: %.1f  std: %.3f  var: %.3f' % (np.mean(cv_scores), np.std(cv_scores), np.var(cv_scores)))
