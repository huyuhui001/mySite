#!/usr/bin/env python 
# -*- coding:utf-8 -*-


class Car:
    # attribute
    price = 0
    owner = ''

    # private attribute
    __Insured = False  # __前缀定义了私有属性

    # Constructor
    def __init__(self, price, owner):  # 用self参数来表示实例
        self.price = price
        self.owner = owner

    # method
    def printInfo(self):  # method第一个参数须指向实例
        print('Owner is:' + self.owner)
        print('price is:' + str(self.price))

    def get_Insured(selfs):
        return selfs.__Insured

    def set_Insured(selfs, Insured):
        selfs.__Insured = Insured

    def start(self):
        self.__startByEngine()
        print("Start Car")

    def __startByEngine(self):
        print("Start Car By Engine")


myCar = Car(250000, 'Peter')
myCar.printInfo()
print(myCar.owner)  # Peter

print(myCar.get_Insured())  # False
myCar.set_Insured(True)  # True

print(myCar.get_Insured())
myCar._Car__Insured = False  # Car里的私有属性__Insured被重命名为_Car__Insured，但不建议这样修改，建议通过get和set方式

print(myCar.get_Insured())  # False
myCar.__Insured = True  # 这里修改的__Insured，并不是Car类里的私有属性__Insured，而是另一个公有属性，所以下面输出__Insured的值仍然是False
print(myCar.get_Insured())  # False

myCar.start()
myCar._Car__startByEngine()  # 不推荐的做法
