#!/usr/bin/env python 
# -*- coding:utf-8 -*-


# Sum Up
def cal_sum(max_num):
    num = 0
    total = 0
    while num <= max_num:
        total = total + num
        num = num + 1
    return total


print(cal_sum(100))  # 5050
print(cal_sum(15.68))  # 120, 向下取整为15


# Recursion
def factorial(input_num):
    if input_num < 0:
        return "error"
    elif input_num == 0:
        return 0
    elif input_num == 1:
        return 1
    return input_num * factorial(input_num - 1)


print(factorial(-1))  # error
print(factorial(0))  # 0
print(factorial(5))  # 120


# Recursion replaced by loop
def factorial_by_loop(input_num):
    start_num = 1
    result_num = 1
    while start_num <= input_num:
        result_num = result_num * start_num
        start_num = start_num + 1
    return result_num


print(factorial_by_loop(-1))  # 1
print(factorial_by_loop(0))  # 1
print(factorial_by_loop(5))  # 120


# Function as input parameters
def add_num(x, y, func):
    return func(x) + func(y)


def square(input_num):
    return input_num * input_num


print(add_num(3, 4, square))  # 自定义square函数
print(add_num(3, -4, abs))  # 预定义函数abs


# Function as return value
def get_cal_func(max_num):
    def sum_up():
        total = 0
        i = 0
        while i <= max_num:
            total = total + i
            i = i + 1
        return total

    return sum_up()


print(get_cal_func(100))  # 5050

func = get_cal_func(100)
print(func)  # 5050
# print(func())  # exception error


# Lambda express 表达式 (anonymous function 匿名函数)
cal_square_sum = lambda x, y: x * x + y * y
print(cal_square_sum(3, 4))  # 25
cal_sumup = lambda x, y, z: x + y + z
print(cal_sumup(3, 4, 5))  # 12
