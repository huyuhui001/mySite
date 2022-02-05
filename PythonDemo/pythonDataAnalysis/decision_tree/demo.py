#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import pydotplus
from six import StringIO


class PredictDiabetes(object):
    @classmethod
    def predict_diabetes(cls):
        data_set = pd.read_csv('pima-indians-diabetes.csv')
        print('=============')
        print(data_set)

        # define feature columns which will be selected for analysis
        feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
        X = data_set[feature_columns]  # get feature column
        y = data_set.label  # get label

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # dtc = DecisionTreeClassifier(criterion='entropy')
        dtc = DecisionTreeClassifier(criterion='gini')
        dtc.fit(X_train, y_train)

        y_pred = dtc.predict(X_test)

        print('=============')
        print(y_test)
        print('=============')
        print(y_pred)
        print('=============')
        print('Accuracy Score: ', accuracy_score(y_test, y_pred))

        # test_data = [5,166,72,19,175,25.8,0.587,51]
        # y_predict = dtc.predict(test_data)  # one sample with multiple features, need use NumPy to reshape
        # y_predict = dtc.predict(np.array(test_data).reshape([1, -1]))
        # print(y_predict)

        dot_data = StringIO()
        export_graphviz(dtc,
                        out_file=dot_data,
                        feature_names=feature_columns,
                        class_names=['0', '1'],
                        filled=True,
                        rounded=True,
                        special_characters=True)  # class_name refers to labels
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf('decision_tree.pdf')


if __name__ == '__main__':
    pds = PredictDiabetes()
    pds.predict_diabetes()
    #PredictDiabetes().predict_diabetes()

''' Demo 1st run
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np


class PredictDiabetes(object):
    @classmethod
    def predict_diabetes(cls):
        data_set = pd.read_csv('pima-indians-diabetes.csv')
        # print(data_set)
        feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
        X = data_set[feature_columns]
        y = data_set.label

        dtc = DecisionTreeClassifier()
        dtc.fit(X, y)
        test_data = [10, 139, 180, 0, 0, 27.1, 1.441, 57]
        y_pred = dtc.predict(np.array(test_data).reshape(1, -1))
        print(y_pred)


if __name__ == "__main__":
    PredictDiabetes.predict_diabetes()
'''

''' Demo 2nd run
class PredictDiabetes(object):
    @classmethod
    def predict_diabetes(cls):
        data_set = pd.read_csv('pima-indians-diabetes.csv')
        # print(data_set)
        feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
        X = data_set[feature_columns]
        y = data_set.label

        dtc = DecisionTreeClassifier()
        dtc.fit(X, y)
        test_data = [10, 139, 180, 0, 0, 27.1, 1.441, 57]
        y_pred = dtc.predict(np.array(test_data).reshape(1, -1))
        print(y_pred)

        dot_data = StringIO()
        export_graphviz(dtc, out_file=dot_data,
                        feature_names=feature_columns,
                        class_names=['0', '1'],
                        filled=True,
                        rounded=True,
                        special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf('decision_tree.pdf')

'''

''' Demo 3rd run
class PredictDiabetes(object):
    @classmethod
    def predict_diabetes(cls):
        data_set = pd.read_csv('pima-indians-diabetes.csv')
        # print(data_set)
        feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
        X = data_set[feature_columns]
        y = data_set.label

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        y_pred = dtc.predict(X_test)
        print(accuracy_score(y_test, y_pred))

        dot_data = StringIO()
        export_graphviz(dtc, out_file=dot_data,
                        feature_names=feature_columns,
                        class_names=['0', '1'],
                        filled=True,
                        rounded=True,
                        special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf('decision_tree.pdf')
'''