print(1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9 * 10)

# =================
result = 1
value = 1

while value <= 10:
    result *= value
    value += 1

print(result, value)

# =================
result = 1
value = 1

for value in range(1, 11):
    result *= value
    value += 1

print(result, value)

# =================
print("Greater"[1])
print("Greater"[-3])
print("Hello" + "Python")
print('A' > 'a')
print('A' < 'a')

# =================
print("Greater"[:])  # 返回字串 Greater
print("Greater"[2:])  # 返回字串 eater
print("Greater"[:2])  # 返回字串 Gr
print("Greater"[2:5])  # 返回字串 eat

# =================
print("%6s" % "four")
print("%-6s" % "four")
#   four
# four

for i in range(7, 11):
    print(i, 10 * i)
# 7 70
# 8 80
# 9 90
# 10 100

for i in range(7, 11):
    print("%-3d%5d" % (i, 10 * i))
# 7     70
# 8     80
# 9     90
# 10   100

for i in range(7, 11):
    print("%-3d%5.3f" % (i, i / 3))
# 7  2.333
# 8  2.667
# 9  3.000
# 10 3.333

print("%6.3f" % 3.14)
#  3.140
print("%-6.3f" % 3.14)
# 3.140
print(3.14)

salary = 100.00
print("Salary: $" + str(salary))
# Salary: $100.0
print("Salary: $%0.2f" % salary)
# Salary: $100.00

# =================

print("greater".isupper())
# 运行结果
# False
print("greater".upper())
# 运行结果
# GREATER
print("greater".startswith("great"))
# 运行结果
# True

print(len("greater"))
print("greater".__len__())
# 运行结果
# 7

print("great" + "er")
print("great".__add__("er"))
# 运行结果
# greater

print("e" in "great")
print("great".__contains__("e"))
# 运行结果
# True

# dir(str)
# help(str.__contains__)

# =================

print("Python is cool".split())
# 运行结果：
# ['Python', 'is', 'cool']
print(" ".join(["Python", "is", "cool"]))
# 运行结果：
# Python is cool

print((21))
# 运行结果：
# 21

print((21, ))
# 运行结果：
# (21,)

# =================
myString = "I love Python"
for i in myString:
    print(i)

myString = "I love Python"
for i in range(len(myString)):
    print(myString[i])

myString = "I love Python"
for i in enumerate(myString):
    print(i)

myString = "I love Python"
for i, j in enumerate(myString):
    print(i, j)

myString = "I love Python"
for i in iter(myString):
    print(i)

myString = "I love Python"
myList = myString.split()
for i in myList:
    print(i)

myList = [67, 100, 'Monday', "It's good"]
for item in myList:
    print(item)

myList = [67, 100, 'Monday', "It's good"]
for idx in range(len(myList)):
    print(myList[idx])

myString = "I love Python"
myList = myString.split()
myTuple = tuple(myList)
for i in myTuple:
    print(i)



myDict = {'name': 'Ming', 'id': 1001, 'age': 35}
print(myDict)

for keys in myDict:
    print(keys, myDict[keys])

# myDict.pop('city')  # 报错，KeyError: 'city'
myDict.pop('id')
print(myDict)
# 运行结果：{'name': 'Ming', 'age': 35}

myString = "I love Python"
myList = myString.split()
print(myList)
print(myList.index('love'))


myString = "I love Python"
myList = myString.split()
myTuple = tuple(myList)
print(myTuple)
print(myTuple.index('love'))

myTuple = (('r', 'g', 'b'), 'hexString')
print(myTuple)
# 运行结果：
# (('r', 'g', 'b'), 'hexString')
print(myTuple[0])
# 运行结果：
# ('r', 'g', 'b')
print(myTuple[0][0])
# 运行结果：
# r
print(myTuple[0][1])
# 运行结果：
# g
print(myTuple[0][2])
# 运行结果：
# b
print(myTuple[1])
# 运行结果：
# hexString


newTuple = (('r', 'g', 'b'), 'hexString')

print(newTuple[0])
# ('r', 'g', 'b')
print(newTuple[0][0])
# 运行结果：
# r
print(newTuple[0][1])
# 运行结果：
# g
print(newTuple[0][2])
# 运行结果：
# b
print(newTuple[1])
# 运行结果：
# hexString




# =================
def square(n): 
    """返回n的平方数""" 
    result = n ** 2 
    return result

print(square(5))






