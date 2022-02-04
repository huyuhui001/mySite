#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt


def load_dataset():
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5)
    return X, y

def define_models():
    models = dict()
    for i in range(1, 21):
        steps = [('pca', PCA(n_components=i)), ('model', LogisticRegression())]
        pipeline = Pipeline(steps=steps)
        models[i] = pipeline
    return models


def evaluate_model(model, X, y):
    rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=3)
    cv_score = cross_val_score(model, X, y, scoring='accuracy', cv=rskf)
    print('mean: %.3f  std: %.3f' % (cv_score.mean(), cv_score.std()))
    return cv_score

# def dimensionality_reduction(X):
#     pca = PCA(n_components=5)
#     X_new = pca.fit_transform(X)
#     return X_new


if __name__ == '__main__':
    X, y = load_dataset()
    # print(X[0])
    # X_new = dimensionality_reduction(X)
    # print(X_new)
    models = define_models()
    components = []
    results = []
    for component, model in models.items():
        cv_score = evaluate_model(model, X, y)
        components.append(component)
        results.append(cv_score)
    plt.boxplot(results, labels=components)
    plt.show()

