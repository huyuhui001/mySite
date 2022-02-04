#!/usr/bin/env python 
# -*- coding:utf-8 -*-


# Basic Data Type
age = 16
print(age + 1)  # 17

returnVal = 0xff
print(returnVal)  # 255

price = 20.8
print(20.8 * 2)  # 41.6

isExpensive = price < 30
print(isExpensive)  # True

lightSpeed = 3e5  # 300,000
print(lightSpeed * 10)  # 3,000,000

oneNm = 1e-9
print(oneNm * 5)  # 5e-09

# Basic String Operation
logMsg = 'in StringDemo.py'
logMsg = logMsg + ",connect String"
print(logMsg)  # in StringDemo.py,connect String

twoLineStr = "first line\nsecond line"
print(twoLineStr)

print(len(logMsg))  # 31
print(logMsg.replace('in', '?'))  # ? Str?gDemo.py,connect Str?g
print(logMsg.find('StringDemo'))  # 3
print(logMsg.find('Not Exist'))  # -1
print(logMsg.index('StringDemo'))  # 3
print(logMsg.index('in'))  # 0 if not matched, will through exception directly, not return -1 like logMsg.find

print(logMsg[0:4])  # in S
print(logMsg[1:4])  # n S
print(logMsg[:5])  # in St
print(logMsg[10:])  # emo.py,connect String
print(logMsg[-1])  # g
print(logMsg[10:-3])  # emo.py,connect Str

newLogMsg = logMsg[0:4]  # in S
newLogMsg = newLogMsg.replace('in', 'for')
print(newLogMsg)  # for S

# if-else
year = 2020
if year % 400 == 0:
    print("是闰年")
elif (year % 4 == 0) and (year % 100 != 0):
    print("是闰年")
else:
    print("不是闰年")

# for-loop
number = '123'
for singleNum in number:  # 遍历number里的每个元素字符
    print(singleNum)
languageArr = ['Python', 'Java', 'Go']  # 遍历languageArr里的每个元素字符
for lang in languageArr:
    print(lang)

# while-loop
# 计算1到101间所有奇数的和
num = 1
total = 0
while num <= 101:
    print(num)
    total = total + num
    num = num + 2
print(total)  # 2601

# break/continue in loop
languageArr = ['Java', 'C++', 'Python', 'Go']
for lang in languageArr:
    print(lang)
    if lang == 'Python':
        break

languageArr = ['Java', 'C++', 'Python', 'Go']
for lang in languageArr:
    if lang == 'C++':
        continue
    else:
        print(lang)

# Format print layout
print('Hello %s, Welcome to %s' % ('Tom', 'Python'))  # Hello Tom, Welcome to Python
print('Hello %s, your age is %d, your price is %f' % (
'Tom', 22, 15000.5))  # Hello Tom, your age is 22, your price is 15000.500000
print('Your price is %.2f' % 15000.5)  # Your price is 15000.50
print('LightSpeed is %e km per second' % 300000)  # LightSpeed is 3.000000e+05 km per second
