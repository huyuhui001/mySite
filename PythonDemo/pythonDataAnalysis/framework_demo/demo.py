#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from sklearn.datasets import make_classification  # generate customized data.
# n_sample (samples number),
# n_features (features number),
# n_informative (meaningful columns),
# n_redundant (redundant columns),
# n_classes(data groups)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt


def load_data():
    return make_classification(n_samples=1000)


def define_models():
    models = dict()
    models['LR'] = LogisticRegression()
    models['KNN'] = KNeighborsClassifier()
    models['DTC'] = DecisionTreeClassifier()
    models['GNB'] = GaussianNB()
    models['SVC'] = SVC()
    return models


def make_pipeline(model):
    steps = list()
    steps.append(('standardize', StandardScaler()))
    steps.append(('normalize', Normalizer()))
    steps.append(('model', model))
    pipeline = Pipeline(steps=steps)
    return pipeline


def evaluate_single_model(X, y, model, fold):
    kfold = KFold(n_splits=fold)
    pipeline = make_pipeline(model)
    cv_score = cross_val_score(pipeline, X, y, cv=kfold, scoring='accuracy')
    return cv_score


def evaluate_models(X, y, models, fold=10):
    results = dict()
    for name, model in models.items():
        cv_score = evaluate_single_model(X, y, model, fold)
        if cv_score is not None:
            results[name] = cv_score
            print('name: %s %f (+/-%f)' % (name, cv_score.mean(), cv_score.std()))
        else:
            print('error')
    return results


if __name__ == '__main__':
    X, y = load_data()
    # print(X)
    # print(y)
    models = define_models()
    # print(models)
    results = evaluate_models(X, y, models)
    plt.boxplot(results.values(), labels=results.keys())
    plt.show()
