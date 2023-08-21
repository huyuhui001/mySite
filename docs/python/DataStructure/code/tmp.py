# =================
# def mySum(lower, upper):
#     """对给定的最小值到最大值之间的整数求和; lower:最小值; upper:最大值;"""
#     result = 0
#     while (lower <= upper):
#         result = result + lower
#         lower += 1
#     return result

# print(mySum(1, 10))
# # 运行结果：
# # 55

# # def mySum(lower, upper):
# #     """对给定的最小值到最大值之间的整数求和; lower:最小值; upper:最大值;"""
# #     if lower <= upper:
# #         return lower + mySum(lower + 1, upper)
# #     else:
# #         return 0

# mySum(1, 10)
# # 运行结果：
# # 55

# def mySum(lower, upper, margin=0):
#     """对给定的最小值到最大值之间的整数求和，通过阶梯方式输出; lower:最小值; upper:最大值;"""
#     blanks = " " * margin
#     print(blanks, lower, upper)

#     if lower <= upper:
#         result = lower + mySum(lower + 1, upper, margin + 4)
#         print(blanks, result)
#         return result
#     else:
#         print(blanks, 0)
#         return 0

# print(mySum(1, 5))
# # 运行结果：
# #  1 5
# #      2 5
# #          3 5
# #              4 5
# #                  5 5
# #                      6 5
# #                      0
# #                  5
# #              9
# #          12
# #      14
# #  15
# # 15

# # 定义inner函数
# def inner():
#     print('我是inner')

# # 定义outer函数，outer函数调用inner函数
# def outer():
#     print('我是outer')
#     inner()

# outer()
# # 运行结果：
# # 我是outer
# # 我是inner

# 定义inner函数

# # 定义outer函数，outer函数内嵌inner函数，并调用inner函数
# def outer():
#     print('我是outer')

#     # 定义inner函数
#     def inner():
#         print('我是inner')

#     inner()

# outer()
# # 运行结果：
# # 我是outer
# # 我是inner

# def outer():
#     a = 1
#     print('我是outer')

#     # 定义inner函数
#     def inner():
#         print('我是inner')
#         print('inner打印: ', a)

#     return inner

# f = outer()
# # 运行结果：
# # 我是outer
# f()
# # 运行结果：
# # 我是inner
# # inner打印:  1

# def outer():
#     a = 1
#     print('我是outer')

#     # 定义inner函数
#     def inner():
#         nonlocal a
#         a += 5
#         print('我是inner')
#         print('inner打印: ', a)

#     return inner

# f = outer()
# # 运行结果：
# # 我是outer
# f()
# # 运行结果：
# # 我是inner
# # inner打印:  6

# # 第一个定义
# def factorial(n):
#     """返回 n 的阶乘"""

#     def recurse(n, product):
#         """计算阶乘的帮助器"""
#         print(n, product)
#         if n == 1:
#             return product
#         else:
#             return recurse(n - 1, n * product)

#     return recurse(n, 1)

# f = factorial(5)
# # f(5, 1)
# # 运行结果
# # 120

# # 第二个定义
# def factorial(n, product=1):
#     """返回 n 的阶乘"""
#     if n == 1:
#         return product
#     else:
#         return factorial(n - 1, n * product)

# print(factorial(5))
# # 运行结果
# # 120

# oldList = [0, 1, 3, 5, 7, 9]
# newList = []

# for i in oldList:
#     newList.append(str(i))

# print(newList)
# # ['0', '1', '3', '5', '7', '9']

# oldList = [0, 1, 3, 5, 7, 9]
# newList = []

# newList = list(map(str, oldList))

# print(newList)
# # ['0', '1', '3', '5', '7', '9']

# oldList = [0, 1, 3, 5, 7, 9]
# newList = []

# for i in oldList:
#     if i > 0:
#         newList.append((str(i)))

# print(newList)
# # ['1', '3', '5', '7', '9']




# oldList = [0, 1, 3, 5, 7, 9]
# newList = []


# def isPositive(n):
#     if n > 0:
#         return True


# newList = list(filter(isPositive, oldList))
# print(newList)
# # [1, 3, 5, 7, 9]



# oldList = [0, 1, 3, 5, 7, 9]
# newList = []

# newList = list(filter(lambda i: i > 0, oldList))

# print(newList)
# # [1, 3, 5, 7, 9]

# import functools

# result = functools.reduce(lambda x, y: x * y, range(1, 11))

# print(result)
# # 3628800
