#!/usr/bin/env python 
# -*- coding:utf-8 -*-


# magic method 魔术方法
class Truck:
    def __init__(self, price):
        print("in __init__")
        self.price = price

    def __del__(self):
        print("in __del__")

    def __str__(self):
        print("in __str__")
        return "price is : " + str(self.price)

    def __repr__(self):
        print("in __repr__")
        return "price is: " + str(self.price)

    def __setattr__(self, name, value):  # 无论属性是否存在，它都允许用户定义对对属性的赋值行为
        print("in __setattr")
        self.__dict__[name] = value

    def __getattr__(self, key):  # 定义当用户试图获取一个不存在的属性时的行为
        print("in __getattr__")
        if key == "price":
            return self.price
        else:
            print("Class has not attribute '%s'" % key)

    def __eq__(self, obj):
        print("in __eq__")
        return self.price == obj.price


myTruck = Truck(10000)  # method __init__ , __setattr__
peterTruck = Truck(20000)  # method __init__ , __setattr__

print(myTruck)  # __str__
myTruck.price = 20000  # price is : 10000  method: __setattr__
print(myTruck == peterTruck)  # True,  method: __eq__

'''sequence of method called
in __init__
in __setattr
in __init__
in __setattr
in __str__
price is : 10000
in __setattr
in __eq__
True
in __del__
in __del__
'''
