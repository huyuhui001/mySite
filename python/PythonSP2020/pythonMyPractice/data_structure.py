#!/usr/bin/env python 
# -*- coding:utf-8 -*-


# list 列表
my_list = ['Python', 'Java', 'Go']
print(my_list)  # ['Python', 'Java', 'Go']

mixed_list = ['Python', True, 20]
print(mixed_list)  # ['Python', True, 20]
print(mixed_list[1])  # 列表的索引是从0开始

my_list.append('C#')  # 追加
print(my_list)  # ['Python', 'Java', 'Go', 'C#']

my_list.extend(mixed_list)  # 合并
print(my_list)  # ['Python', 'Java', 'Go', 'C#', 'Python', True, 20]

my_list.insert(3, 'new')  # 插入
print(my_list)  # 在第3号索引位插入，之后的元素位顺延。['Python', 'Java', 'Go', 'new', 'C#', 'Python', True, 20]

my_list.remove('new')  # 删除
print(my_list)  # ['Python', 'Java', 'Go', 'C#', 'Python', True, 20]

del my_list[5]  # 删除
print(my_list)  # ['Python', 'Java', 'Go', 'C#', 'Python', 20]

my_list[3] = 0x56  # 替换
print(my_list)  # ['Python', 'Java', 'Go', 86, 'Python', 20]

# list slice 列表切片是指将一个列表分割成多个列表
id_list = [1, 2, 3, 4, 5, 6]
print(id_list[0:2])  # [1, 2]
print(id_list[3:])  # [4, 5, 6]
print(id_list[:3])  # [1, 2, 3]
print(id_list[1:-2])  # [2, 3, 4]
new_id_list = id_list[0:2]
id_list[0] = 100
print(id_list)  # [100, 2, 3, 4, 5, 6]
print(new_id_list)  # [1, 2]

price_list = [100.5, 200.8, 150.7]
for price in price_list:
    print(price)
for cnt in range(len(price_list)):
    print(cnt, price_list[cnt])
for cnt, element in enumerate(price_list):
    print(cnt, element)

print(len(my_list))  # 6
print(my_list.count('Go'))  # 1，Go在list中出现的次数
print(my_list.index('Go'))  # 2
new_my_list = my_list.copy()
print(new_my_list)

new_my_list.reverse()
print(new_my_list)
print(new_my_list.reverse())  # None  区别：reverse()方法本身没返回值

# Tuple 元组 和列表的区别是--不可变
list1 = ['a', 'b', 6.5, 'lock', 3.14, 'e']
tuple1 = ('A', 'B', 2.01, 'C', 'D')
print(list1)  # ['a', 'b', 6.5, 'lock', 3.14, 'e']
print(tuple1)  # ('A', 'B', 2.01, 'C', 'D')

print(list1[2])  # 6.5
print(tuple1[2])  # 2.01

converted_list = list(tuple1)
print(converted_list)  # ['A', 'B', 2.01, 'C', 'D']
print(converted_list[2])  # 2.01

converted_tuple = tuple(list1)
print(converted_tuple)  # ('a', 'b', 6.5, 'lock', 3.14, 'e')
print(converted_tuple[2])  # 6.5

print('e' in list1)  # True. False if not

for i in list1:
    print(i)

for j in tuple1:
    print(j)

# Set 集合
emp_ids = {101, 103, 99, 104, 99, 101}
print(emp_ids)  # {104, 99, 101, 103}  实现去除重复

emp_ids.add(102)
print(emp_ids)  # {99, 101, 102, 103, 104}

emp_ids.add(99)
print(emp_ids)  # {99, 101, 102, 103, 104}

# empID.remove(1000)  # exception
emp_ids.discard(1000)  # no exception

emp_ids.remove(101)
print(emp_ids)  # {99, 102, 103, 104}
print(len(emp_ids))  # 4

emp_ids.clear()
print(emp_ids)  # 输出空集合 set()
print(len(emp_ids))  # 0

# Operation of
set_from_mem = set([10, 12, 14, 8])
set_from_file = {10, 3, 8, 15}

# 遍历
for i in set_from_file:
    print(i)

# 交集
print(set_from_mem & set_from_file)  # {8, 10}
print(set_from_mem.intersection(set_from_file))  # {8, 10}

# 并集
print(set_from_mem | set_from_file)  # {3, 8, 10, 12, 14, 15}
print(set_from_mem.union(set_from_file))  # {3, 8, 10, 12, 14, 15}

# 差集
print(set_from_mem - set_from_file)  # {12, 14} 存在于set_from_mem集合但不存在于set_from_file集合的元素
print(set_from_mem.difference(set_from_file))  # {12, 14}
print(set_from_file - set_from_mem)  # {3, 15} 存在于set_from_file集合但不存在于set_from_mem集合的元素
print(set_from_file.difference(set_from_mem))  # {3, 15}

# Dictionary 字典 键值对 Key-Value Pair
scoreDict = {'Java': 95, 'Python': 100, 'C#': 96}
print(scoreDict['Python'])  # 100

dupDict = {'Java': 95, 'Python': 100, 'C#': 96, 'Java': 97}
print(dupDict['Java'])  # 97  后面的97会替换掉前面的95
# print(scoreDict['Go'])  # exception: KeyError: 'Go'

scoreDict['Go'] = 98  # Insert
print(scoreDict)

scoreDict['Java'] = 92  # Update
print(scoreDict)
scoreDict.update({'Python': 89})  # Update
print(scoreDict)
scoreDict.update({'C++': 65})  # Update, 如果key不存在，则执行insert
print(scoreDict)

del scoreDict['C++']  # Delete, 如果key值不存在，exception
print(scoreDict)

for i in scoreDict:
    print(i)  # 只输出keys
    print(scoreDict[i])  # 只输出value
    print(i + ":" + str(scoreDict[i]))

for j in scoreDict.items():
    print(j)

for (keys, values) in scoreDict.items():
    print(keys + ":" + str(values))


# map方法实现序列的映射
def increase(x):
    return x + 1


new_list = map(increase, [1, 2, 3])
print(new_list)  # <map object at 0x0000019E14B41F70>
print(list(new_list))  # [2, 3, 4]


def tag_student(score):
    if score > 90:
        return "good"
    return "normal"


new_list = map(tag_student, [100])
print(list(new_list))  # ['good']
new_list = map(tag_student, [80])
print(list(new_list))  # ['normal']
new_list = map(tag_student, [100, 80])
print(list(new_list))  # ['good', 'normal']

total = map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6])
print(total)  # <map object at 0x0000025B7A121EE0>
print(list(total))  # [5, 7, 9]


# filter方法实现数据筛选
def check_even_num(num):
    return num % 2 == 0  # 把判断条件写在return中


output_list = filter(check_even_num, [1, 2, 3, 4])
print(list(output_list))  # [2, 4]
output_list = filter(lambda x: x % 2 == 0, [1, 2, 3, 4])
print(list(output_list))  # [2, 4]

# reduce方法实现累计
from functools import reduce


def add(x, y):
    return x + y


result = reduce(add, [1, 2, 3])
print(result)  # 6
result = reduce(add, [1, 2, 3], 9)  # 第3个参数带有个初始值9
print(result)  # 15


def multiply(x, y):
    return x * y


result = reduce(multiply, [1, 2, 3])
print(result)  # 6
result = reduce(multiply, [1, 2, 3], 10)  # 第3个参数带有个初始值10
print(result)  # 60
result = reduce(lambda x, y: x * y, [1, 2, 3], 10)
print(result)  # 60

# sorted方法排序
score = [98, 57, 100, 95]
print(sorted(score))  # [57, 95, 98, 100]
print(sorted(score, reverse=True))  # [100, 98, 95, 57]

employees = [('Tom', 10000, 'B'), ('Peter', 9000, 'A'), ('John', 15000, 'C')]
sorted_by_salary = sorted(employees, key=lambda x: x[1])  # x[1]是每个维度的第2个数，即 ('Tom', 10000, 'B')中索引1的值排序-salary
print(sorted_by_salary)  # [('Peter', 9000, 'A'), ('Tom', 10000, 'B'), ('John', 15000, 'C')]
sorted_by_name = sorted(employees, key=lambda x: x[0], reverse=True)
print(sorted_by_name)  # [('Tom', 10000, 'B'), ('Peter', 9000, 'A'), ('John', 15000, 'C')]
