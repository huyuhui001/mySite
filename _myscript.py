#!/usr/bin/env python3
# -*-coding:utf-8 -*-


from bisect import bisect
from re import S, T
from subprocess import call
from matplotlib import collections
from numpy import arange, vectorize
from pandas import array
from pandas_datareader import test
from sklearn.metrics import jaccard_score

# =================================================================
# color = ['Black', 'White']
# size = ['S', 'M', 'L']
# tshirts = [{i: j} for i in color for j in size]
# print(tshirts)


# =================================================================
# symbols = 'abcd'
# code = [ord(symbol) for symbol in symbols]
# print(code)

# =================================================================
# x, y, *rest, = arange(10)
# print(x, y, rest)

# print(y)
# print(rest)


# =================================================================
# def maker(n):
#     k = 8
#     def action(x):
#        return x + n + k
#     return action

# f = maker(2) 
# print(f(3))
# print(f(4))
# print(f(5))



# =================================================================
# def get_money():
#     money = 0

#     def work():
#         nonlocal money
#         money += 100
#         print(money)

#     return work


# closure = get_money()

# closure()



# =================================================================
# from collections import namedtuple

# City = namedtuple('City', 'name country population coordinates')

# tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139691667))

# print(tokyo)
# # City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139691667))

# print(tokyo.population)
# # 36.933

# print(tokyo[3])
# # (35.689722, 139691667)

# # _fields属性是一个包含这个类所有字段名称的元组。
# print(City._fields)
# # ('name', 'country', 'population', 'coordinates')

# LatLong = namedtuple('LatLong', 'lat long')

# delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613899, 77.208889))

# # 用_make()通过接受一个可迭代对象来生成这个类的一个实例，它的作用跟City(*delhi_data)是一样的。
# delhi = City._make(delhi_data)

# print(delhi)
# # City(name='Delhi NCR', country='IN', population=21.935, coordinates=LatLong(lat=28.613899, long=77.208889))

# # _asdict()把具名元组以collections.OrderedDict的形式返回，我们可以利用它来把元组里的信息友好地呈现出来。
# print(delhi._asdict())
# # OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population', 21.935), ('coordinates', LatLong(lat=28.613899, long=77.208889))])

# for key, value in delhi._asdict().items():
#     print(key + ':', value)

# # name: Delhi NCR
# # country: IN
# # population: 21.935
# # coordinates: LatLong(lat=28.613899, long=77.208889)



# =================================================================
# invoice = """
# 0     6                                 40           52   55
# 1909  Primoroni PiBrella                $17.50       3    $52.50
# 1489  6mm Tactile Switch x20            $4.19        2    $9.90
# 1510  Panavise JR.-PV-201               $28.00       1    $28.00
# 1601  PiTFT Mini Kit 320x240            $34.95       1    $34.95
# """

# SKU = slice(0, 6)
# DESCRIPTION = slice(6, 40)
# UNIT_PRICE = slice(40, 52)
# QUANTITY = slice(52, 55)
# ITEM_TOTAL = slice(55, None)

# line_items = invoice.split('\n')[2:]  # 按上面invoice的格式，第0和1行舍弃

# for item in line_items:
#     print(item[UNIT_PRICE], item[DESCRIPTION])

# # $17.50       Primoroni PiBrella                
# # $4.19        6mm Tactile Switch x20            
# # $28.00       Panavise JR.-PV-201               
# # $34.95       PiTFT Mini Kit 320x240 



# =================================================================

# board = [['_'] * 3 for i in range(3)]
# print(board)
# # [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

# board[1][2] = 'X'
# print(board)
# # [['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]


# board = [['_'] * 3] * 3
# print(board)
# # [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

# board[1][2] = 'X'
# print(board)
# # [['_', '_', 'X'], ['_', '_', 'X'], ['_', '_', 'X']]




# =================================================================

# row = ['_'] * 3
# board = []

# for i in range(3):
#     board.append(row)

# print(board)
# # [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

# board[2][0] = 'X'
# print(board)
# # [['X', '_', '_'], ['X', '_', '_'], ['X', '_', '_']]


# row = []
# board = []

# for i in range(3):
#     row = ['_'] * 3
#     board.append(row)

# print(board)
# # [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

# board[2][0] = 'X'
# print(board)
# # [['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]




# =================================================================

# list1 = [1, 2, 3, 4]
# id(list1)
# # 140409777308808

# list1 *= 2
# print(list1)
# # [1, 2, 3, 4, 1, 2, 3, 4]
# id(list1)
# # 140409777308808


# tuple1 = (1, 2, 3, 4)
# id(tuple1)
# # 140409777230536

# tuple1 *= 2
# print(tuple1)
# # (1, 2, 3, 4, 1, 2, 3, 4)
# id(tuple1)
# # 140409780104888


# =================================================================
# t = (1, 2, [10, 20])

# t[2] += [50, 60]
# # TypeError: 'tuple' object does not support item assignment

# print(t)
# # (1, 2, [10, 20, 50, 60])


# dis.dis('s[a] += b')






# =================================================================


# list1 = ['1', 'one', '3', 'Four', '5', 'two', 'apple', '8', '9']

# print(list1)
# # ['1', 'one', '3', 'Four', '5', 'two', 'apple', '8', '9']

# print(sorted(list1))
# # ['1', '3', '5', '8', '9', 'Four', 'apple', 'one', 'two']
# print(sorted(list1, reverse=True))
# # ['two', 'one', 'apple', 'Four', '9', '8', '5', '3', '1']
# print(sorted(list1, key=len))
# # ['1', '3', '5', '8', '9', 'one', 'two', 'Four', 'apple']
# print(list1)
# # ['1', 'one', '3', 'Four', '5', 'two', 'apple', '8', '9']


# print(list1.sort())
# # None
# print(list1)
# # ['1', '3', '5', '8', '9', 'Four', 'apple', 'one', 'two']





# =================================================================
# import bisect

# def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
#     i = bisect.bisect(breakpoints, score)
#     return grades[i]

# [grade(score) for score in [15, 26, 31, 62, 79, 85]]
# # ['F', 'F', 'F', 'D', 'C', 'B']





# =================================================================
# import bisect
# import random

# size = 7
# random.seed(1729)
# my_list = []

# for i in range(size):
#     new_item = random.randrange(size*2)
#     bisect.insort(my_list, new_item)
#     print(f'{new_item:2d} :--> {my_list}')

# # 10 :--> [10]
# #  0 :--> [0, 10]
# #  6 :--> [0, 6, 10]
# #  8 :--> [0, 6, 8, 10]
# #  7 :--> [0, 6, 7, 8, 10]
# #  2 :--> [0, 2, 6, 7, 8, 10]
# # 10 :--> [0, 2, 6, 7, 8, 10, 10]


# =================================================================

# from array import array

# numbers = array('h', [-2, -1, 0, 1, 2])
# # array('h', [-2, -1, 0, 1, 2])

# memv = memoryview(numbers)
# print(len(memv))
# # 5
# print(memv[0])
# # -2
# print(memv.tolist())
# # [-2, -1, 0, 1, 2]

# memv_oct = memv.cast('B')
# print(memv_oct.tolist())
# # [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]

# memv_oct[5] = 4
# print(numbers)
# # array('h', [-2, -1, 1024, 1, 2])







# =================================================================
# from collections import deque

# d = deque([1, 2, 3])
# print(d)
# # deque([1, 2, 3])

# # 注意插入顺序
# d.extendleft(['a', 'b', 'c'])
# print(d)
# # deque(['c', 'b', 'a', 1, 2, 3])

# print(len(d))
# # 6
# print(d[-2])
# # 2

# # 统计字符a出现的次数
# print(d.count('a'))
# # 1

# # 返回字符a的索引值
# print(d.index('a'))
# # 2

# # 第0位插入数字1，其余顺移
# d.insert(0, 1)
# print(d)
# # deque([1, 'c', 'b', 'a', 1, 2, 3])

# # 把右边2个元素放到左边，注意顺序，和extendleft不一样
# d.rotate(2)
# print(d)
# # deque([2, 3, 1, 'c', 'b', 'a', 1])

# d.rotate(-2)
# print(d)
# # deque([1, 'c', 'b', 'a', 1, 2, 3])



# =================================================================

# a = dict(one=1, two=2, three=3)
# b = {'one': 1, 'two': 2, 'three': 3}
# c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
# d = dict([('two', 2), ('three', 3), ('one', 1)])
# e = dict({'three': 3, 'one': 1, 'two': 2})

# print(a == b == c == d == e)
# # True




# =================================================================

# words = ['apple', 'bat', 'bar', 'atom', 'book']

# by_letter = {}

# for word in words:
#     letter = word[0]  # word[0]的输出依然是5个列表元素的首字母a, b, b, a, b
#     by_letter.setdefault(letter, []).append(word)  # 如果letter不在[]则通过append添加word

# print(by_letter)  
# # {'a': ['apple', 'atom'], 'b': ['bat', 'bar', 'book']}




# =================================================================

# str = 'abracadabra'
# ct = collections.Counter(str)

# print(ct)
# # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})



# =================================================================

# from types import MappingProxyType

# d = {1: 'A'}
# d_proxy = MappingProxyType(d)

# print(d)
# # {1: 'A'}
# print(d_proxy)
# # {1: 'A'}

# print(d[1])
# # A
# print(d_proxy[1])
# # A


# d[2] = 'W'
# print(d)
# # {1: 'A', 2: 'W'}

# d_proxy[2] = 'W'
# # TypeError: 'mappingproxy' object does not support item assignment

# print(d_proxy)
# # {1: 'A', 2: 'W'}





# =================================================================

# haystacke = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'f', 'g', 'h', 'c', 'd', 'e', 'c', 'd', 'e', 'f', 'g', 'h'}
# needles = {'c', 'h', 'w'}

# type(haystacke)
# # <class 'set'>
# type(needles)
# # <class 'set'>


# found = 0

# for i in needles:
#     if i in haystacke:
#         found += 1

# print(found)
# # 2


# found = len(needles & haystacke)
# print(found)
# # 2

# found = len(needles.intersection(haystacke))
# print(found)
# # 2





# =================================================================

# cafe = bytes('cafe', encoding='utf-8')
# print(cafe)
# # b'cafe'
# print(cafe[:1])
# # b'c'

# cafe_array = bytearray(cafe)
# print(cafe_array)
# # bytearray(b'cafe')
# print(cafe_array[:1])
# # bytearray(b'c')



# =================================================================

# BingoCage类的实例使用任何可迭代对象构建，而且会在内部存储一个随机顺序排列的列表。调用实例会取出一个元素。
# import random

# class BingoCage:
#     def __init__(self, item):
#         self._item = list(item)
#         random.shuffle(self._item)

#     def pick(self):
#         try:
#             return self._item.pop()
#         except IndexError:
#             raise LookupError('pick from empty BingCage')

#     def __call__(self):
#         return self.pick()


# bingo = BingoCage(range(3))

# bingo.pick()
# bingo()

# callable(bingo)
# # True

# bingo.__dict__
# # {'_item': [0, 1]}
# bingo.__dir__()
# # ['_item', '__module__', '__init__', 'pick', '__call__', '__dict__', '__weakref__', '__doc__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']





# class C: 
#     pass

# obj = C()

# def func():
#     pass

# sorted(set(dir(obj)) - set(dir(func)))
# # ['__weakref__']
# sorted(set(dir(func)) - set(dir(obj)))
# # ['__annotations__', '__call__', '__closure__', '__code__', '__defaults__', '__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']





# =================================================================


# def clip(text:str, max_len:'int > 0'=80) -> str:
#     """
#     Get sub-string by the first blank before or after specified position.
#     rfind() 返回字符串最后一次出现的位置，如果没有匹配项则返回 -1.
#     """
#     end = None

#     if len(text) > max_len:
#         space_before = text.rfind(' ', 0, max_len)

#         if space_before >= 0:
#             end = space_before
#     else:
#         space_after = text.rfind(' ', max_len)

#         if space_after >= 0:
#             end = space_after
    
#     if end is None:
#         end = len(text)
    
#     return text[:end].rstrip()



# clip('This is the string', max_len=10)
# # 'This is'

# clip.__annotations__
# # {'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}


# clip.__defaults__
# # (80,)

# clip.__code__
# # <code object clip at 0x7f1e04a5c8a0, file "<stdin>", line 1>

# clip.__code__.co_varnames
# # ('text', 'max_len', 'end', 'space_before', 'space_after')

# clip.__code__.co_argcount
# # 2

# clip.__doc__
# # '\n    Get sub-string by the first blank before or after specified position.\n    rfind() 返回字符串最后一次出现的位置，如果没有匹配项则返回 -1.\n    '



# from inspect import signature

# sig = signature(clip)

# type(sig)
# # <class 'inspect.Signature'>
# print(sig)
# # (text, max_len=80)
# print(str(sig))
# # (text, max_len=80)

# for name, param in sig.parameters.items():
#     print(f'{param.kind} : {name} = {param.default}')

# # 1 : text = <class 'inspect._empty'>
# # 1 : max_len = 80

# print(sig.return_annotation)
# # <class 'str'>

# for param in sig.parameters.values():
#     note = repr(param.annotation).ljust(13)
#     print(f'{note} : {param.name} = {param.default}')

# # <class 'str'> : text = <class 'inspect._empty'>
# # 'int > 0'     : max_len = 80






# =================================================================

# registry = []

# def register(func):
#     print(f'running register {func}')
#     registry.append(func)
#     return func

# @register
# def f1():
#     print('running f1()')

# @register
# def f2():
#     print('running f2()')

# def f3():
#     print('running f3()')

# def main():
#     print('runnning main()')
#     print(f'registry--> {registry}')
#     f1()
#     f2()
#     f3()

# if __name__ == '__main__':
#     main()





# =================================================================

# # 计算移动平均值的类
# class Avg():

#     def __init__(self):
#         self.mylist = []

#     def __call__(self, newValue):
#         self.mylist.append(newValue)
#         total = sum(self.mylist)
#         return total/len(self.mylist)


# avg = Avg()

# avg(10)
# # 10.0
# avg(20)
# # 15.0
# avg(30)
# # 20.0


# def make_avg():

#     my_list = []

#     def avg(newValue):
#         my_list.append(newValue)
#         total = sum(my_list)
#         return total/len(my_list)
    
#     return avg

# my_avg = make_avg()

# my_avg(10)
# # 10.0
# my_avg(20)
# # 15.0
# my_avg(30)
# # 20.0

# my_avg.__code__.co_varnames
# # ('newValue', 'total')

# my_avg.__code__.co_freevars
# # ('my_list',)

# my_avg.__closure__
# # (<cell at 0x7fe93d347468: list object at 0x7fe93d0e2f48>,)

# my_avg.__closure__[0].cell_contents
# # [10, 20, 30]
# my_avg.__closure__[1].cell_contents




# def make_avg():
#     count = 0
#     total = 0

#     def avg(newValue):
#         nonlocal count, total
#         count += 1
#         total += newValue
#         return total / count
    
#     return avg


# my_avg = make_avg()

# my_avg(10)
# # 10.0
# my_avg(20)
# # 15.0
# my_avg(30)
# # 20.0

# my_avg.__code__.co_varnames
# # ('newValue',)

# my_avg.__code__.co_freevars
# # ('count', 'total')

# my_avg.__closure__
# # (<cell at 0x7fe93d3474c8: int object at 0x7fe93e865240>, <cell at 0x7fe93d347318: int object at 0x7fe93e865960>)

# my_avg.__closure__[0].cell_contents
# # 3
# my_avg.__closure__[1].cell_contents
# # 60


# =================================================================

# def get_money():
#     money = 0

#     def work():
#         nonlocal money
#         money += 100
#         print(money)

#     return work


# closure = get_money()

# closure()
# # 100
# closure()
# # 200
# closure()
# # 300



# =================================================================

from array import array
import math

class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)



v1 = Vector2d(3, 4)

v1.__abs__()
v1.__repr__()


Vector2d(3, 4).frombytes()


