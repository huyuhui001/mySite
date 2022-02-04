#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import os
import sys

# print("__file__", __file__)
# # C:\Python\Python37\python.exe C:/myProjects/myPython/pythonMyPractice/example/temp.py


# print(sys.path[0])
# # C:\myProjects\myPython\pythonMyPractice\example


# print(*[1, 2, 3])
# # 1 2 3

# 两两判断True/False，都为True，整个表达式为True
print(3 < 5 > 3)  # True
print(3 < 5 > 6)  # False
print(5 < 5 > 6)  # False
print(3 < 5 < 7)  # True
print(3 < 5 > 3 < 5)  # True

# 从左向右，输出第一个False的值，否则输出最右边的值
print(3 and 5 and 7)  # 7
print(3 and 5 and 0)  # 0
print(3 and 0 and 7)  # 0
# 从左向右，输出第一个True的值
print(0 or 5 or 9)  # 5
print(3 or 5 or 9)  # 3
print(0 or 0 or 9)  # 9
print(0 or 0 or 0)  # 0
#
#
#
#
# print(3 & 5)


s = [{1, 2}, {3, 4}]
t = [{1}, {2}]
print(sub(s))


# x = [1, 2, 3]
# print(x)
# x.append(8)
# print(x)
# x.insert(0, 9)
# print(x)
# x = x + [7]
# print(x)
# # [1, 2, 3]
# # [1, 2, 3, 8]
# # [9, 1, 2, 3, 8]
# # [9, 1, 2, 3, 8, 7]


# str = 'Hello world!'
# str.ljust(15, '0')
# print(str.ljust(15, '0'))
# l = len('Hello world!'.ljust(50))
# print(l)
# Hello world!000
# 50


# import random
# x = random.sample(range(10), 5)
# print(x)


# x = [3, 5, 3, 7]
# y = [x.index(i) for i in x if i == 3]
# print(y)
# y = [x.index(i) for i in x if i < 9]
# print(y)
# y = [x.index(i) for i in x if i <= 3]
# print(y)
# y = [x.index(7)]
# print(y)
# # [0, 0]
# # [0, 1, 0, 3]
# # [0, 0]
# # [3]


# x = sum(range(1, 10, 2))  # range(start, stop[, step])
# print(x)  # 1+3+7+9=25


# import numpy.linalg


# print(not 3)
# # False


# y = abs(3 + 4j)
# print(y)
# # 5.0


# z = callable(int)
# print(z)
# # True


# x = 3 & 6  # 0011 & 0110
# print(x)
# # 2


# x = 16 ** 0.5
# print(x)
# # 4.0


# x = type({3})
# print(x)
# # <class 'set'>


# x = isinstance('Hello world', str)
# print(x)
# # True
