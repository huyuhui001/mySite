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

# def getYourAge(prompt):
#     """提示用户输入一个整数，否则给出错误提示，并继续提示用户输入。"""
#     inputStr = input(prompt)
#     try:
#         number = int(inputStr)
#         return number
#     except ValueError:
#         print("Error in number format:", inputStr)
#         return getYourAge(prompt)

# if __name__ == "__main__":
#     age = getYourAge("Enter your age: ")
#     print("Your age is", age)

# # 运行结果
# # Enter your age: 3a
# # Error in number format: 3a
# # Enter your age: 3.5
# # Error in number format: 3.5
# # Enter your age: 20
# # Your age is 20

# import random

# f = open("./docs/python/DataStructure/code/myfile.txt", 'w')

# for count in range(500):
#     number = random.randint(1, 500)
#     f.write(str(number) + "\n")

# f.close()

# import random

# f = open("./docs/python/DataStructure/code/myfile.txt", 'w')

# f.write("first line.\nSecond line.\n")  # 初始化文件内容
# f.close()

# # 打开文件读取内容
# f = open("./docs/python/DataStructure/code/myfile.txt", 'r')

# text1 = f.read()  # 把文件的全部内容输入单个字符串中
# print(text1)
# # 运行结果：
# # first line.
# # Second line

# text2 = f.read()  # 再次read，得到一个空字串，表述已经到达文件末尾。要再次读取需要重新打开文件
# print("======")
# print(text2)
# # 运行结果：
# # ======
# #

# f.close()

# # 重新打开文件读取内容
# f = open("./docs/python/DataStructure/code/myfile.txt", 'r')

# for line in f:  # 逐行读取文件内容
#     print("======")
#     print(line)  # 每行都有一个换行符，这是print函数默认行为

# # 运行结果：
# # ======
# # first line.

# # ======
# # Second line.
# #

# f.close()

# # 重新打开文件读取内容
# f = open("./docs/python/DataStructure/code/myfile.txt", 'r')

# while True:
#     line = f.readline()  # readline方法会从输入的文本里只获取一行数据，并且返回这个包含换行符的字符串。如果readline遇到了文件末尾，那么会返回空字符串。
#     if line == "":
#         break
#     print("******")
#     print(line)

# # 运行结果：
# # ******
# # first line.

# # ******
# # Second line.
# #

# f.close()

# # 重新打开文件读取内容
# f = open("./docs/python/DataStructure/code/myfile.txt", 'r')

# line = f.readlines()  # readlines方法则是读取所有行，返回的是所有行组成的列表。
# print(line)
# # 运行结果：
# # ['first line.\n', 'Second line.\n']

# f.close()

# ========================================
# import random

# f = open("./docs/python/DataStructure/code/myfile.txt", 'w')

# # 生成0~9整数，并写入文件
# for count in range(10):
#     f.write(str(count) + "\n")

# f.close()

# # 打开文件
# f = open("./docs/python/DataStructure/code/myfile.txt", 'r')

# # 依次读取文件中的数字，并求和
# theSum = 0
# for line in f:
#     line = line.strip()
#     number = int(line)
#     theSum += number

# print("The sum is : ", theSum)
# # 运行结果：
# # The sum is :  45

# f.close()

# ========================================
# import random
#
# # 打开文件
# f = open("./docs/python/DataStructure/code/myfile.txt", 'r')

# # 依次读取文件中的数字，并求和
# theSum = 0
# for line in f:
#     lines = line.split()  # split方法会自动处理换行符
#     for word in lines:
#         number = int(word)
#         theSum += number

# print("The sum is : ", theSum)
# # 运行结果：
# # The sum is :  53286

# f.close()

# ========================================
# import random

# f = open("./docs/python/DataStructure/code/myfile.txt", 'r')
# print("The sum is: ", sum(map(int, f.read().split())))
# # 运行结果：
# # The sum is :  53286

# f.close()

# ========================================
# import pickle

# myList = [60, "A string object", 1977]

# fObj = open("./docs/python/DataStructure/code/items.dat", "wb")

# for item in myList:
#     pickle.dump(item, fObj)

# fObj.close()

# ===========================
# import pickle

# lyst = list()
# fileObj = open("./docs/python/DataStructure/code/items.dat", "rb")
# while True:
#     try:
#         item = pickle.load(fileObj)
#         lyst.append(item)
#     except EOFError:  # 检测已经到达文件末尾
#         fileObj.close()
#         break
# print(lyst)
# # 运行结果：
# # [60, 'A string object', 1977]



# ============================
class Counter(object):    # Counter类是object的子类
    """Models a counter."""

    # Class variable 类变量
    instances = 0         # 跟踪已创建的计数器对象的数量

    # Constructor 构造器
    # 实例方法__init__也称为构造函数；这个方法用来初始化实例变量，并且对类变量进行更新；
    def __init__(self):   # self是指在运行时这个方法的对象本身
        """Sets up the counter."""
        Counter.instances += 1
        self.reset()

    # Mutator methods
    def reset(self):
        """Sets the counter to 0."""
        self.value = 0

    def increment(self, amount = 1):
        """Adds amount to the counter."""
        self.value += amount

    def decrement(self, amount = 1):
        """Subtracts amount from the counter."""
        self.value -= amount

    # Accessor methods
    def getValue(self):
        """Returns the counter's value."""
        return self.value

    def __str__(self):
        """Returns the string representation of the counter."""
        return str(self._value) 

    def __eq__(self, other):
        """Returns True if self equals other
        or False otherwise."""
        if self is other: return True
        if type(self) != type(other): return False
        return self.value == other.value

from collections import Counter

from counter import Counter
c1 = Counter()
print(c1)
0
c1.getValue()
0
str(c1)
'0'
c1.increment()
print(c1)
1
c1.increment(5)
print(c1)
6
c1.reset()
print(c1)
0
c2 = Counter()
Counter.instances
2
c1 == c1
True
c1 == 0
False
c1 == c2
True
c2.increment()
c1 == c2
False

