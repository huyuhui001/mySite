#!/usr/bin/env python 
# -*- coding:utf-8 -*-


# polymorphism 多态
# 在Python里，多态的主要表现形式是“可变参数”
# 在使用过程中，多态往往和继承一起使用
# 在下面两个类里，__iter__和__next__两方法名相同，都是遍历，而实现细节不同，多态特性。
class VisitNumber:
    def __init__(self, max):
        self.value = 0
        self.max = max

    def __iter__(self):  # 返回self，即实例的本身
        return self

    def __next__(self):  # 定义了访问实例中下一个元素的方法
        if self.value == self.max:
            raise StopIteration()
        self.value += 1
        return self.value


print("******************** separator *****************")


class VisitString:
    def __init__(self, str):
        self.str = str
        self.num = len(str)
        self.startNum = -1

    def __iter__(self):  # 返回self，即实例的本身
        return self

    def __next__(self):  # 定义了访问实例中下一个元素的方法
        self.startNum += 1
        if self.startNum >= self.num:
            raise StopIteration()
        return self.str[self.startNum]


myNumList = VisitNumber(3)
for i in myNumList:
    print(i)
'''
1
2
3
'''

print("******************** separator *****************")

myStrList = VisitString("Hello")
for i in myStrList:
    print(i)
'''
H
e
l
l
o
'''

print("******************** separator *****************")


# 可变参数与方法重载
class PrintTool:
    def printInfo(self):
        print("Print in default mode")

    def printInfo(self, modeName):
        print("Print in " + modeName + " mode")

    def printWithParam(self, *args):  # *args可变参数，在调用时，以元组的形式传入参数，实现重载，体现多态
        print(args)

    def printWithDict(self, **kwargs):  # **kwargs可变参数，在调用时，以字典的形式传入参数，实现重载，体现多态
        print(kwargs)


tool = PrintTool()
# tool.printInfo()  # 报错，需要输入参数
tool.printInfo("Canon")  # Print in Canon mode
tool.printWithParam('No.123', 'A4')  # ('No.123', 'A4')
tool.printWithParam('No.123', 'A4', 'Now')  # ('No.123', 'A4', 'Now')
tool.printWithDict(printNo='No.123', printMode='A4')  # {'printNo': 'No.123', 'printMode': 'A4'}
tool.printWithDict(printNo='No.123', printMode='A4',
                   printTime='Now')  # {'printNo': 'No.123', 'printMode': 'A4', 'printTime': 'Now'}

print("******************** separator *****************")


# 整合使用多态和继承
class Emp:
    def work(self):
        print("Work as Emp Mode")


class PythonDev(Emp):
    def work(self):  # 重写父类方法，定义Python开发的工作方式
        print("Develop Python")


class HR(Emp):
    def work(self):  # 重写父类方法，定义HR的工作方式
        print("Do HR job")


pythonDev = PythonDev()
hr = HR()
pythonDev.work()  # Develop Python
hr.work()  # Do HR job
