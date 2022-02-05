#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# position arguments
# *args: non-keyword arguments, () tuple
# **kwargs: keyword arguments, {key=value, ...} dict
# *, name: keyword only arguments
# default Value
# list[]

class Employee(object):
    def __init__(self, code, name, *, salary=0.0, **kwargs):
        self.code = code
        self.name = name
        self.salary = salary
        self.details = kwargs
        print(kwargs)


if __name__ == '__main__':
    data = {'email': 'email@mail.cn', 'phone': '123-456-789'}
    employee = Employee('E01', 'Jacky', salary=5.6, **data)
    print(employee.code, employee.name, employee.salary)
    print(employee.details.get('email'))
    print(employee.details.get('phone'))
