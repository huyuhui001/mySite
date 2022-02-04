#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# This is to get general understanding of frequent Itemsets (频繁项目集) via Apriori Algorithm
# 先找频繁项集，再根据关联规则找关联物品

from mlxtend.preprocessing import TransactionEncoder  # Encoder class for transaction data in Python lists
from mlxtend.frequent_patterns import apriori
import pandas as pd

# ====== Data Set ======
data_set = [['Apple', 'Beer', 'Rice', 'Chicken'],
            ['Apple', 'Beer', 'Rice'],
            ['Apple', 'Beer'],
            ['Apple', 'Bananas'],
            ['Milk', 'Beer', 'Rice', 'Chicken'],
            ['Milk', 'Beer', 'Rice'],
            ['Milk', 'Beer'],
            ['Apple', 'Bananas']]
print("-----print original dataset------")
print(data_set)

""" ====== Fit and encode data ======
Use two methods, fit and transform of TransactionEncoder to let mlxtend know
all unique value and encode them to one-hot code
"""
te = TransactionEncoder()
array = te.fit_transform(data_set)

print("-----print te.columns_------")
print(te.columns_)  # After fit, mlxtend knows all unique value from dataset.
print("-----print array------")
print(array)  # After transform, mlxtend encode data to one-hot code (True-False)
print("-----print array (different layout)------")
print(array.astype('int'))  # After transform, mlxtend encode data to one-hot code (1-0)

""" ====== Form data into Padas DataFrame ======
DataFrame
    是一种表格型数据结构，它含有一组有序的列，每列可以是不同的值。
    DataFrame既有行索引，也有列索引，它可以看作是由Series组成的字典，不过这些Series公用一个索引。
    DataFrame的创建有多种方式，不过最重要的还是根据dict进行创建，以及读取csv或者txt文件来创建。
"""
df = pd.DataFrame(data=array, columns=te.columns_)

# Get frequent itemsets from a one-hot DataFrame
# min_support: a float between 0 and 1 for minumum support of the itemsets (最小关联度) returned.
frequent_item_set = apriori(df, min_support=0.6, use_colnames=True)
print(frequent_item_set)  # Return all support value (关联度) >= 0.6
