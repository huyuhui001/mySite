#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn

data_set = pd.read_csv('employee_data.csv')
# print(data_set)

# Bar: number of projects
number_projects = data_set.groupby('number_project').count()
print(number_projects)

plt.bar(number_projects.index.values, number_projects['salary'])
plt.xlabel('number of project')
plt.ylabel('number of employee')
plt.show()

# Bar: time_spend_company
number_projects = data_set.groupby('time_spend_company').count()
print(number_projects)

plt.bar(number_projects.index.values, number_projects['salary'])
plt.xlabel('Number of years spend in company')
plt.ylabel('number of employee')
plt.show()

# Bar: Departments
number_projects = data_set.groupby('Departments').count()
print(number_projects)

plt.bar(number_projects.index.values, number_projects['salary'])
plt.xlabel('Number of Departments')
plt.ylabel('number of employee')
plt.show()

# Bar: Salary
number_projects = data_set.groupby('salary').count()
print(number_projects)

plt.bar(number_projects.index.values, number_projects['satisfaction_level'])
plt.xlabel('Rage of Salary')
plt.ylabel('number of employee')
plt.show()

features = ['number_project', 'time_spend_company', 'Departments', 'salary']
for i, j in enumerate(features):  # i: each chart in above features, j: x-axis in each chart
    plt.subplot(3, 2, i + 1)  # 3 rows, 2 columns in the combined chart output
    seaborn.countplot(x=j, data=data_set)
    plt.subplots_adjust(hspace=0.5)
    plt.xticks(rotation=45)
plt.show()


''' Demo 1st run
import pandas as pd
import matplotlib.pyplot as plt

data_set = pd.read_csv('employee_data.csv')
# print(data_set)
number_projects = data_set.groupby('number_project').count()
print(number_projects)
plt.bar(number_projects.index.values, number_projects['satisfaction_level'])
plt.xlabel('number of project')
plt.ylabel('number of employee')
plt.show()
'''
