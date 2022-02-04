#!/usr/bin/env python 
# -*- coding:utf-8 -*-
'''
常用异常处理类一览表
ArithmeticError	数值计算错误的基类
FloatingPointError	浮点计算错误时触发
ZeroDivisionError	除数为零时会触发
AttributeError	访问到类实例不存在的属性时，会触发
TypeError	调用函数时，参数类型不正确时会触发
ValueError	调用函数时，返回值不正确时会触发
IOError	输入输出失败时会触发
'''

empIDList = ['1', '2', '3']
try:
    print(empIDList[3])
except IndexError:
    print("Index Error")  # 输出
else:
    print("Continue, no exception")

try:
    100 + '$'
except TypeError:
    print("Type Error")  # 输出
finally:  # 不管是否发生异常，或者不管发生何种异常，都需要被执行
    print("divided by 0 in finally")  # 输出

try:
    1 / 0
except TypeError:
    print("Type error in divided 0")  # 不输出
except ZeroDivisionError:
    print("Zero Division Error")  # 输出
else:
    print("1/0, continue, no exception")  # 不输出

print("******************** separator *****************")


# try:
#     1 / 0
# except TypeError:
#     print("Type error, divided by 0")  # 不输出
# else:
#     print("1/0, continue, no exception")  # 程序终止，不执行else


def calAvg(total, number):
    try:
        return total / number
    except(ZeroDivisionError, TypeError, Exception) as e:
        print(e)


print(calAvg(100, 2))  # 50.0
print(calAvg(100, 0))  # division by zero  ; None  引发除0异常，本身打印None --total / number
print(calAvg(100,
             '2'))  # unsupported operand type(s) for /: 'int' and 'str'   ; None   引发TypeError，本身打印None --total / number
print('continue................')

print("******************** separator *****************")


class OrderBusinessException(Exception):
    def __init__(self, msg, errorCode, email):
        self.msg = msg
        self.errorCode = errorCode
        self.email = email


def handeOrder(name, number):
    if number <= 0:
        raise OrderBusinessException('Order Number is less than 0', '100', 'xx@mail.cn')
    else:
        print('handle order correctly')


try:
    handeOrder('Python Book', -1)  # 触发异常
except OrderBusinessException as e:
    print(e.msg)
    print(e.errorCode)
    print(e.email)
except Exception as e:  # 用Exception来兜底
    print(e)
print('continue')
'''输出结果
Order Number is less than 0
100
xx@mail.cn
continue
'''

print("******************** separator *****************")

empSalaryDic = [{'name': 'Mike', 'salary': 10000}, {'name': 'Tom', 'salary': '15000'},
                {'name': 'John', 'salary': 12000}]
try:
    for item in empSalaryDic:
        item['salary'] = item['salary'] * 1.1  # 每人工资增长10%
except Exception as e:
    print(e)
    print('error, name is: ' + item['name'])

print(empSalaryDic)
'''
can't multiply sequence by non-int of type 'float'
error, name is: Tom
[{'name': 'Mike', 'salary': 11000.0}, {'name': 'Tom', 'salary': '15000'}, {'name': 'John', 'salary': 12000}]

由于Tom的数据错误，导致处理中断，John这条记录没有被处理
'''

print("******************** separator *****************")

empSalaryDic = [{'name': 'Mike', 'salary': 10000}, {'name': 'Tom', 'salary': '15000'},
                {'name': 'John', 'salary': 12000}]

for item in empSalaryDic:
    try:
        item['salary'] = item['salary'] * 1.1  # 每人工资增长10%
    except Exception as e:
        print(e)
        print('error, name is: ' + item['name'])

print(empSalaryDic)
'''
can't multiply sequence by non-int of type 'float'
error, name is: Tom
[{'name': 'Mike', 'salary': 11000.0}, {'name': 'Tom', 'salary': '15000'}, {'name': 'John', 'salary': 13200.000000000002}]

虽然Tom的数据错误，抛出异常后继续处理John这条记录
'''

print("******************** separator *****************")

# 文件读写的异常机制

import os

print(os.path.abspath('/opt/projects/myPython/temp_files'))  # /opt/projects/myPython/temp_files
print(os.path.exists('/opt/projects/myPython/temp_files'))  # True

print(os.path.abspath('/opt/projects/myPython/temp_file'))  # 不存在，仍然显示
print(os.path.exists('/opt/projects/myPython/temp_file'))  # False

print(os.path.abspath('/opt/projects/myPython/temp_files/hello1.txt'))  # 不存在，仍然显示
print(os.path.exists('/opt/projects/myPython/temp_files/hello1.txt'))  # False

print(os.listdir('/opt/projects/myPython/temp_files/'))  # ['hello.txt']

print(os.path.isdir('/opt/projects/myPython/temp_files/hello.txt'))  # False
print(os.path.isfile('/opt/projects/myPython/temp_files/hello.txt'))  # Ture 如果存在，则返回True，否则返回False

print(os.path.split(
    '/opt/projects/myPython/temp_files/hello.txt'))  # 返回一个元组 ('/opt/projects/myPython/temp_files', 'hello.txt')

print("******************** separator *****************")

# 文件打开/关闭操作
filename = '/opt/projects/myPython/temp_files/hello.txt'
try:
    file = open(filename, mode='r')
    print(file.read())
except Exception as e:
    print(e)
finally:
    if 'file' in locals().keys():
        print('Close the file')
        file.close()
print('Continue......')
file.close()

print(
    locals().keys())

'''
Hello Python...
I am learning it now...

Close the file
Continue......
dict_keys(['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__annotations__', '__builtins__', '__file__', '__cached__', 'empIDList', 'calAvg', 'OrderBusinessException', 'handeOrder', 'empSalaryDic', 'item', 'os', 'filename', 'file'])
'''

print("******************** separator *****************")

# 文件读取操作
try:
    file = open(filename, mode='r+')
    line_read = file.readline()
    while line_read:
        try:
            line_read = line_read
            print(line_read, end='')
            line_read = file.readline()
        except Exception as e:
            print("error when reading line")
            continue
except Exception as e:
    print(e)
finally:
    try:
        print('close file')
        file.close()
    except Exception as e:
        print('error when closing the file')
        print(e)

print('Now adding new lines into the file......')

try:
    file = open(filename, mode='a+')  # append model
    file.writelines('add new line. \n')
except Exception as e:
    print('error when writing')
finally:
    try:
        file.close()
    except Exception as e:
        print(e)

'''
Hello Python...
I am learning it now...
close file
Now adding new lines into the file......
'''

print("******************** separator *****************")

# Write CSV file
import csv

head = ['empID', 'empName', 'empSalary']
emp1 = ['E01', 'Jason', '10000']
emp2 = ['E02', 'Jack', '15000']

try:
    file = open('/opt/projects/myPython/temp_files/emp.csv', 'w+', newline='')  # writerow方法在写完内容时会自动换行
    write = csv.writer(file)
    write.writerow(head)  # It's fun if use write.writerows(head), each word is a row, letters are separated by comma
    write.writerow(emp1)
    write.writerow(emp2)
except Exception as e:
    print(e)
finally:
    if file in locals().keys():
        file.close()

# Read CSV file
try:
    file2 = open('/opt/projects/myPython/temp_files/emp.csv', 'r')
    reader = csv.reader(file2)
    for row in reader:
        print(row)   # failed on this step. bypassed??
except Exception as e:
    print("Error when Reading Csv file.")
    print(e)
finally:
    if file2 in locals().keys():
        file2.close()
'''
Failed
'''
