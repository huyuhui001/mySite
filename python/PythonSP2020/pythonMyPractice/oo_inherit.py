#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# Inheritance 继承
class Emp:
    _accountBalace = 1000  # 前缀 _ 定义“受保护”的属性和方法

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __getApproval(self):
        print("Before add salary, get Approval.")

    def work(self):
        print("Emp work")

    def addSalary(self, number):
        self.__getApproval()
        self.salary = self.salary + number

    def _useAccount(self, number):
        if self._accountBalace >= number:
            print("Can use")
        else:
            print("Can not use")

    def printInfo(self):
        print("name is: " + self.name + " , salary is: " + str(self.salary))


class PythonDeveloper(Emp):  # PythonDeveloper继承Emp， 使用父类的__init__方法
    def work(self):
        print("develop python")

    def learnPython(self):
        print(self.name + " learn Python.")


class Developer(Emp):
    def teamBuilding(self, number):
        self._useAccount(number)


class AnotherCompanyDeveloper():
    def __init__(self, name):
        self.name = name

    def teamBuilding(self, number):
        self._useAccount(number)


pythonDev = PythonDeveloper('Peter', 12000)
pythonDev.printInfo()  # name is: Peter , salary is: 12000
pythonDev.learnPython()  # Peter learn Python.
pythonDev.addSalary(5000)
pythonDev.printInfo()  # name is: Peter , salary is: 17000
pythonDev.work()  # develop python

myEmp = Emp("Jason", 15000)
myEmp.printInfo()  # name is: Jason , salary is: 15000
pythonDev._Emp__getApproval()  # Before add salary, get Approval.  _pythonDev__getApproval()不存在，因为无法继承
myEmp._Emp__getApproval()  # Before add salary, get Approval.  不推荐直接访问。

developer = Developer('John', 15000)
developer.printInfo()  # name is: John , salary is: 15000
developer._useAccount(1000)  # Can use 不推荐直接访问
developer.teamBuilding(1002)  # Can not use

anoDev = AnotherCompanyDeveloper('Wang')

# anoDev.teamBuilding(1000)  # 报错，anoDev不是emp的子类

print("******************** separator *****************")


# 多重继承
class PrintByA3:
    def print(self):
        print("print file in A3")


class PrintByA4:
    def print(self):
        print("print file in A4")


class PrintHandler(PrintByA3, PrintByA4):  # 同时继承了两个类
    def handleFile(self):
        print(self)


handler = PrintHandler()
handler.print()  # print file in A3 多重继承时，次序在前的类方法会覆盖掉之后的

print("******************** separator *****************")


# 用组合模式取代多重继承
class PrintByA3_new:
    def print(self):
        print("print file in A3")


class PrintByA4_new:
    def print(self):
        print("print file in A4")


class PrintHandler_new():
    def __init__(self):
        self.PrintByA3 = PrintByA3_new
        self.PrintByA4 = PrintByA4_new

    def handlerFileAsA3(self):
        self.PrintByA3.print(self)

    def handlerFileAsA4(self):
        self.PrintByA4.print(self)


handler_new = PrintHandler_new()
handler_new.handlerFileAsA3()  # print file in A3
handler_new.handlerFileAsA4()  # print file in A4
