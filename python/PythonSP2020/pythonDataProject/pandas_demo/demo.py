#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pandas as pd

data_set = pd.read_excel('data.xlsx', sheet_name='Sheet1')
print(data_set)

