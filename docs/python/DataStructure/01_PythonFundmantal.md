# 基础知识回顾

## 1.基本程序要素

示例代码`numberguess.py`。

```python
import random

def main():
    smaller = int(input("输入最小值: "))
    larger = int(input("输入最大值: "))
    myNumber = random.randint(smaller, larger)
    count = 0
    while True:
        count += 1
        userNumber = int(input("输入你猜的值: "))
        if userNumber < myNumber:
            print("你猜的太小！")
        elif userNumber > myNumber:
            print("你猜的太大！")
        else:
            print("恭喜，你在第", count, "次猜对了!")
            break

if __name__ == "__main__":
    main()
```

运行代码：

```bash
$ python3 numberguess.py 
Enter the smaller number: 10
Enter the larger number: 60
Enter your guess: 50
Too large
Enter your guess: 40
Too large
Enter your guess: 30
Too large
Enter your guess: 20
Too large
Enter your guess: 10
Too small
Enter your guess: 15
You’ve got it in 6 tries!
```

### 1.1.拼写和命名惯例

- 变量：salary，hoursWorked，isAbsent
- 常数：ABSOLUTE_ZERO，INTEREST_RATE
- 函数或方法：printResults，cubeRoot，input
- 类：BankAccount，SortedSet

通常约定：变量名是名词、形容词（布尔值），函数和方法是动词（表示动作）、名词、或形容词（表示返回的值）。

语法元素：

- Python使用空白符（空格、制表符、或换行符）来表示不同类型的语句的语法。
- 通常约定使用4个空格作为锁进宽度。

### 1.2.字符串

- 单引号
- 双引号
- 成对的三个双引号（多行文本）
- 成对的三个单引号（多行文本）
- 转义字符`\`（反斜杠）

### 1.3.运算符和表达式

- 标准运算符：`+`、`-`、`*`、`/`、`%`
- 算术表达式是用标准运算符和中缀表示法
- 比较运算符：`<`、`<=`、`>`、`>=`、`==`、`!=`，用于比较数字或字符串，返回True或False
- 运算符`==`用于比较数据结构里的内容，运算符`is`用于比较两个对象的标识是否一致
- 逻辑运算符：`and`、`or`、`not`。把0、None、空字符串、空列表等视为False，大多数其他值是为True
- 下标运算符：`[]`，与多项集collection对象一起使用
- 选择器运算符：`.`，用于引用一个模块、类或对象中的一个具名的项

运算符优先级，依次是选择运算符、函数调用运算符、下标运算符、算术运算符、比较运算符、逻辑运算符、赋值运算符。括号用于让子表达式优先运行。

### 1.4.函数调用

函数名称后面跟着用括号括起来的参数列表，例如：`min(5,2)`

- 标准函数
- 其他模块导入函数

### 1.5.`print`函数

- 自动为每个参数运行`str`函数，以得到其字符串表示
- 在输出之前会用空格吧每个字符串隔开
- 默认以换行符作为结束

### 1.6.input函数

- 标准输入函数input会一直等待用户通过键盘输入文本
- 接受一个可选的字符串作为其参数

### 1.7.类型转换函数和混合模式操作

- Python允许算术表达式中的操作数具有不同的数值类型。例如，把int类型的操作数和float类型的操作数相加，会得到float类型的数。

```python
# 输入半径求圆面积
radius = float(input("Radius: "))
print("The area is", 3.14 * radius ** 2)
```

### 1.8.可选和关键字函数参数

- 必选参数是没有默认值的；可选参数有默认值；
- 在调用函数时，传递给它的参数数量必须至少和必选参数的数量相同。
- 标准函数和Python的库函数在调用时都会对传入的参数进行类型检查

### 1.9.变量和赋值语句

- 简单的赋值语句 `PI = 3.1416`
- 多变量赋值 `minValue, maxValue = 1, 100`
- 变量交换 `a, b = b, a`
- 赋值语句必须写在一行代码里，但是可以在逗号、圆括号、花括号或方括号之后换行，或者用转义符`\`进行换行。

换行示例：

```python
minValue = min(100,
               200)
product = max(100, 200) \
          * 30
```

### 1.10.数据类型

- 变量都可以被指定为任何类型的值。这些变量并不像其他语言那样被声明为特定的类型，而只是被赋了一个值
- 值和对象都是有类型的，会在运行时进行数据类型检查

### 1.11.`import`语句

- `import`语句使得一个模块中的标识符可以被另一个程序所见到。标识符可以是对象名、函数名或类名
- 导入模块名称，例如 `import math`
- 导入模块中的标识符，例如：`from math import sqrt`，或者`from math import pi, sqrt`
- 也可以使用符号`*`导入一个模块中的所有名称，但不推荐

## 2.控制语句

### 2.1.条件语句

- 单向if语句的语法

```python
if <Boolean expression>:
    <sequence of statements>
```

- 双向if语句的语法

```python
if <Boolean expression>:
    <sequence of statements>
else:
    <sequence of statements>
```

- 多向if语句的语法

```python
if <Boolean expression>:
    <sequence of statements>
elif <Boolean expression>:
    <sequence of statements>
...
else:
    <sequence of statements>
```

### 2.2.使用if __name__ == "__main__"

示例代码`numberguess.py`。

```python
import random

def main():
    smaller = int(input("输入最小值: "))
    larger = int(input("输入最大值: "))
    myNumber = random.randint(smaller, larger)
    count = 0
    while True:
        count += 1
        userNumber = int(input("输入你猜的值: "))
        if userNumber < myNumber:
            print("你猜的太小！")
        elif userNumber > myNumber:
            print("你猜的太大！")
        else:
            print("恭喜，你在第", count, "次猜对了!")
            break

if __name__ == "__main__":
    main()
```

上面的if语句的作用是，

- 要么将模块当作一个独立的程序运行，该模块的`_name_`变量会设置为字符串`_main_`，才会执行`main()`函数
- 要么从另一个模块中导入，该模块的`_name_`变量会设置该模块的名称，上例中即`numberguess`

### 2.3.循环语句

通常：

- 一般会使用for循环来迭代确定范围的值或值的序列
- 如果继续循环的条件是某个布尔表达式，一般会使用while循环

`while`语法格式：

```python
while <Boolean expression>: 
    <sequence of statements>
```

示例：

```python
# 计算从1到10的乘积并输出结果
result = 1
value = 1

while value <= 10:
    result *= value
    value += 1

print(result, value)

# 运行结果
# 3628800 11
```

`for`语法格式：

```python
for <variable> in <iterable object>:
    <sequence of statements>
```

示例：

```python
# 计算从1到10的乘积并输出结果
result = 1
value = 1

for value in range(1, 11):
    result *= value
    value += 1

print(result, value)

# 运行结果
# 3628800 11
```

## 3.字符串及其运算

- Python中的字符串也是一个复合对象
- Python的字符串类型名为`str`

约定：

- 把单字符的字符串用单引号括起来
- 把多字符的字符串用双引号括起来

### 3.1.运算符

- 比较运算符，是按照ASCII码的顺序比较两个字符串中每个位置的字符对

示例：

```python
print('A' > 'a')
# 运行结果 False

print('A' < 'a')
# 运行结果 True
```

- `+`运算符生成并返回一个包含两个操作数的新字符串

示例：

```python
print("Hello" + "Python")
# 运行结果 HelloPython
```

- 下标运算符，范围是从0到字符串的长度减去1的一个整数。

运算符返回在字符串中该位置的字符。

示例：

```python
print("Greater"[1])
# 运行结果：r
```

当索引为负值时，Python会把这个值和字符串的长度相加，以确定要返回的字符的位置。负索引值不得小于字符串长度的负值。

```python
print("Greater"[-3])
# 运行结果：t

print("Greater"[-9])
# 运行结果：IndexError: string index out of range
```

- 切片运算符（slice operator），下标运算符的一种变体。

语法格式：`<a string>[<lower>:<upper>]`

- `<lower>`：范围是从0到字符串的长度减去1的整数
- `<upper>`：范围是从0到字符串的长度的整数

切片检索规则：

- 返回这样一个子字符串：这个子字符串会从`<lower>`索引处的字符开始，到`<upper>`索引减1的位置作为结束。
- 如果省略`<lower>`索引，那么切片运算符将返回一个以当前字符串的第一个字符作为开头的子字符串。
- 如果省略`<upper>`索引，那么切片运算符将返回一个以当前字符串的最后一个字符作为结尾的子字符串。
- 如果省略这两个值，那么切片运算符会返回整个字符串。

示例：

```python
print("Greater"[:])     # 返回字串 Greater 
print("Greater"[2:])    # 返回字串 eater
print("Greater"[:2])    # 返回字串 Gr
print("Greater"[2:5])   # 返回字串 eat
```

### 3.2.字符串格式化

- 格式化字符串里的数据字符以及满足给定基准线的附加空格的总数称为它的字段宽度（field width）。
- `print`函数会在遇到第一列时自动开始打印输出基准线。

示例，通过print语句输出2列。

```python
for i in range(7, 11):
    print(i, 10*i)

# 运行结果
# 7 70
# 8 80
# 9 90
# 10 100
```

- Python的通用格式化机制
  - 语法格式`<format string> % <datum>` 和 `<format string> % (<datum-1>, …, <datum-n>)`。
  - 格式化字符串时，`<format string>`使用`%<field width>s`表示法。当字段宽度为正时，数据是右对齐的；当字段宽度为负时，数据是左对齐的。
  - 格式整数时，`<format string>`使用`%<field width>d`表示法。
  - 格式浮点数时，`<format string>`使用`%<field width>.<precision>f`表示法，其中`.<precision>`这一部分是可选的。

示例：

```python
print("%6s" % "four")
print("%-6s" % "four")
#   four
# four
```

```python
for i in range(7, 11):
    print("%-3d%5d" % (i, 10*i))
# 7     70
# 8     80
# 9     90
# 10   100
```

```python
for i in range(7, 11):
    print("%-3d%5.3f" % (i, i/3))
# 7  2.333
# 8  2.667
# 9  3.000
# 10 3.333
```

下例对比了浮点数在使用了格式字符串和没有使用格式字符串这两种情况下的输出差异。

```python
salary = 100.00
print("Salary: $" + str(salary))
# Salary: $100.0
print("Salary: $%0.2f" % salary)
# Salary: $100.00
```

注意，下例中Python给数字添加了一个精度位数，并且其左侧填充空格，从而实现了字段宽度为6、精度为3的设置。这个宽度包含小数点后所占据的位置。

```python
print("%6.3f" % 3.14) # 左侧填充了空格
#  3.140
print("%-6.3f" % 3.14)
# 3.140
```

### 3.3.对象和方法调用

语法格式：`<object>.<method name>(<list of arguments>)`

示例：

```python
print("greater".isupper())
# 运行结果
# False 
print("greater".upper())
# 运行结果
# GREATER
print("greater".startswith("great"))
# 运行结果
# True
```

```python
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
```

提示：

1. `dir()`方法会返回所传递的对象的有效属性，语法格式：`dir(object)`
2. `help()`函数查看函数或模块用途的详细说明，语法格式：`help(object)`

```python
dir(str)
help(str.__contains__)
```

## 4.内置多项集及其操作

Python中的多项集（collections）指能够包含元素的数据结构。多项集模块提供了不同类型的容器。容器是用于存储不同对象并提供访问所包含对象以及对它们进行迭代的方式的对象。一些内置的容器有元组（Tuple）、列表（List）、字典（Dictionary）等。

以下是由collections模块提供的不同容器的列表：

- 计数器（Counters）
- 有序字典（OrderedDict）
- 默认字典（DefaultDict）
- 链映射（ChainMap）
- 命名元组（NamedTuple）
- 双向队列（DeQue）
- 用户字典（UserDict）
- 用户列表（UserList）
- 用户字符串（UserString）

### 4.1.列表

列表（list）是零个或多个Python对象的一个序列，这些对象通常称为项（item）。

列表的表现形式是：用方括号括起整个列表，并用逗号分隔元素。

示例：

```python
[]                             # 空列表
["greater", "less", 10]        # 含不同类型的列表
["greater", ["less", 10]]      # 含内嵌列表的列表
```

列表的切片操作：

- 和字符串类似，可以通过标准运算符执行切片或连接操作，返回结果也是列表。
- 和字符串不同，列表是可变的，即，可以替换、插入或删除列表中所包含的项。
  - 切片和连接运算符所返回的列表是新的列表，而不是最初列表的一部分；
  - 列表类型包含了几个叫作变异器（mutator）的方法，用于修改列表的结构。

可以通过`dir(list)`来查看方法，包括变异器（mutator）的方法。

```python
dir(list)
# 运行结果
# ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```

最常用的列表变异器方法是`append`、`insert`、`pop`、`remove`和`sort`。

示例：

```python
myList = []              # myList当前为[] 
myList.append(34)        # myList当前为[34]，默认尾部插入
myList.append(22)        # myList当前为[34, 22]，默认尾部插入
myList.sort()            # myList当前为[22, 34]
myList.pop()             # 默认从索引位[0]删除，返回结果22；myList当前为[34]
myList.insert(0, 22)     # 在指定索引位[0]插入；myList当前为[22, 34]
myList.insert(1, 55)     # 在指定索引位[1]插入；myList当前为[22, 55, 34]
myList.pop(1)            # 指定索引位[1]删除，返回结果55；myList当前为[22, 34]
myList.remove(22)        # 删除首个匹配项的元素[22]；myList当前为[34]
myList.remove(55)        # 报ValueError错，list.remove(x): x not in list
```

对于字符串，split方法会从字符串里分离出一个单词列表，而join方法会把单词列表连在一起从而形成字符串。例如：

```python
print("Python is cool".split())
# 运行结果：
# ['Python', 'is', 'cool']
print(" ".join(["Python", "is", "cool"]))
# 运行结果：
# Python is cool
```

对于列表特性和操作的详细练习，参考[Python语言基础@github](../Foundation/ch01.md)或者[Python语言基础@web](https://huyuhui001.github.io/mySite/python/Foundation/ch01/#13-list)中“1.3 列表（list）”的内容。

### 4.2.元组

元组（tuple）是一个不可变的元素序列。

- 元组（tuple）形式是用圆括号将各项括起来，并且必须至少包含两个项。
- 元组实际上就像列表一样，只不过它没有变异器方法。
- 如果要使元组只包含一个元素，则必须在元组里包含逗号。

对比下面的区别：

```python
print((21))   # (21)被视为整数
# 运行结果：
# 21

print((21,))  # (21,)被视为元组
# 运行结果：
# (21,)
```

对于列表特性和操作的详细练习，参考[Python语言基础@github](../Foundation/ch01.md)或者[Python语言基础@web](https://huyuhui001.github.io/mySite/python/Foundation/ch01/#16-tuple)中“1.6 元组（tuple）”的内容。

### 4.3.序列遍历

`for`循环可以用来遍历序列（如字符串、列表或元组）里的所有元素。

遍历列表：

```python
myList = [67, 100, 'Monday', "It's good"]
for item in myList:
    print(item)

myList = [67, 100, 'Monday', "It's good"]
for idx in range(len(myList)):
    print(myList[idx])
```

遍历元组：

```python
myString = "I love Python"
myList = myString.split()
myTuple = tuple(myList)
for i in myTuple:
    print(i)
```

遍历字符串：(注意，是遍历字符，不是单词)

```python
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
```

如果按照单词遍历字符串，则需要先把字串按单词拆解为列表。

```python
myString = "I love Python"
myList = "I love Python".split()
for i in myList:
    print(i)
```

对于列表和元组遍历的更多例子，包括拆包遍历，参考[Python语言基础@github](../Foundation/ch01.md)或者[Python语言基础@web](https://huyuhui001.github.io/mySite/python/Foundation/ch01/)的内容。

### 4.4.字典

字典（dictionary）包含零个或多个条目。

- 每个条目（entry）都有唯一的键和它所对应的值相关联。
- 键通常是字符串或整数，而值是任意的Python对象。
- 下标运算符可以用于访问一个给定键的值，给一个新键添加一个值，以及替换给定键的值。
- `pop`方法会删除一个条目并返回给定键所对应的值。
- `keys`方法会把所有键返回成一个可迭代对象。
- `values`方法会把所有值返回成一个可迭代对象。

示例：

```python
{}                                      # 空字典
{"name":"Ken"}                          # 含一个条目
{"name":"Ken", "age":67}                # 含二个条目
{"hobbies":["reading", "running"]}      # 含一个条目，其中值是一个列表
```

- 字典本身也是一个可迭代对象。可以通过for语句进行遍历键或/和值。

```python
myDict = {'name': 'Ming', 'id': 1001, 'age': 35}
for keys in myDict:
    print(keys, myDict[keys])
# 运行结果：
# name Ming
# id 1001
# age 35
```

### 4.5.值检索

- 可以在字符串列表、元组或字典里通过`in`运算符来对值或多项集进行搜索，返回`True`或`False`。对于字典来说，搜索的目标值应该是一个键。
- 如果已知给定值存在于序列（字符串、列表或元组）里，那么`index`方法将返回这个值所出现的第一个位置。

列表检索：

```python
myString = "I love Python"
myList = myString.split()
print(myList)
# 运行结果：
# ['I', 'love', 'Python']
print(myList.index('love'))
# 运行结果：
# 1
```

元组检索：

```python
myString = "I love Python"
myList = myString.split()
myTuple = tuple(myList)
print(myTuple)
print(myTuple.index('love'))
```

字典检索：

```python
myDict = {'name': 'Ming', 'id': 1001, 'age': 35}
print(myDict)

for keys in myDict:
    print(keys, myDict[keys])

myDict.pop('city')  # 报错，KeyError: 'city'
myDict.pop('id')
print(myDict)
# 运行结果：{'name': 'Ming', 'age': 35}
```

### 4.6.模式匹配访问多项集

- 下标运算符可以用来访问列表、元组和字典里的元素。
- 通过模式匹配可以一次访问多个元素。

示例：`myTuple`是一个含内嵌元组的元组。

```python
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
```

通过上面的拆解，我们清楚了内嵌元组的结构详细情况。

下面，我们通过模式匹配，把一个结构分配给形式完全相同的另一个结构。这里目标结构`newTuple`所包含的变量从源结构`(('r', 'g', 'b'), 'hexString')`里的相应位置处获得对应的值。

```python
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
```

## 5.创建函数

Python支持完全函数式编程设计。

- Python包含很多内置函数。
- Python也运行创建新函数，可以使用递归，把函数作为数据进行传递和返回。

### 5.1.函数定义

函数定义语法：

- 命名函数名称和参数名称的规则与惯例与命名变量的是相同的。
- 必选参数的列表可以为空，也可以包含用逗号隔开的名称。
- 与其他编程语言不同的是，参数名称或函数名称本身并不会和数据类型进行关联。

```python
def <function name>(<list of parameters>):
    <sequence of statements>
```

示例：

- 在函数的标题下有一行用三引号括起来的字符串`返回n的平方数`，这是一个文档字符串（docstring）。
  - 在shell里面输入help(square)时，会显示这个字符串。
  - 定义的每一个函数都应该有文档字符串，来说明该函数的功能，并提供相关的所有参数以及返回值的信息。
- 函数的参数和临时变量只会在函数调用的生存周期内存在，并且对其他函数及其外围程序都是不可见的。
  - `n`是参数。
  - `result`是临时变量。
- 如果函数不包含`return`语句时，它将在最后一条语句执行之后自动返回`None`值。
- 用`<parameter name> = <default value>`把参数指定为有默认值的可选参数。
- 在参数列表中，必选参数（没有默认值的参数）必须位于可选参数之前。

```python
def square(n): 
    """返回n的平方数""" 
    result = n ** 2 
    return result

print(square(5))
```

### 5.2.函数递归

递归函数（recursive function）是指会调用自身的函数。

为了防止函数无限地重复调用自身，代码中必须至少有一条用来查验条件的选择语句，用于确定接下来要继续递归还是停止递归。这个检查条件语句称为基本情况（base case）。

示例：下面是通过循环实现输出从给定的最小值到最大值之间的整数和。

```python
def mySum(lower, upper):
    """对给定的最小值到最大值之间的整数求和; lower:最小值; upper:最大值;"""
    result = 0
    while (lower <= upper):
        result = result + lower
        lower += 1
    return result


print(mySum(1, 10))
# 运行结果：
# 55
```

用递归函数改写上述函数。

```python
def mySum(lower, upper):
    """对给定的最小值到最大值之间的整数求和; lower:最小值; upper:最大值;"""
    if lower <= upper:
        return lower + mySum(lower + 1, upper)
    else:
        return 0


print(mySum(1, 10))
# 运行结果：
# 55
```

通常来说，递归函数至少有一个参数。

- 这个参数的值会被用来对递归过程的基本情况进行判定，从而决定是否要结束整个调用。
- 在每次递归调用之前，这个值也会被进行某种方式的修改。
- 每次对这个值的修改，都应该产生一个新数据值，可以让函数最终达到基本情况。

为了对`mySum`函数的递归进行跟踪，可以尝试添加一个代表缩进边距的参数并且添加一些print语句。这样在每次调用时，函数的第一条语句会计算缩进数量，然后再打印两个参数的值，每次返回调用之前的返回值时都使用相同的缩进，就可以实现对两个参数的值以及每次调用的返回值进行跟踪。

```python
def mySum(lower, upper, margin=0):
    """对给定的最小值到最大值之间的整数求和，通过阶梯方式输出; lower:最小值; upper:最大值;"""
    blanks = " " * margin
    print(blanks, lower, upper)

    if lower <= upper:
        result = lower + mySum(lower + 1, upper, margin + 4)
        print(blanks, result)
        return result
    else:
        print(blanks, 0)
        return 0


print(mySum(1, 5))
# 运行结果：
#  1 5
#      2 5
#          3 5
#              4 5
#                  5 5
#                      6 5
#                      0
#                  5
#              9
#          12
#      14
#  15
# 15
```

### 5.3.函数嵌套

嵌套函数类似于嵌套循环，就是函数内又嵌套着函数。即，函数的定义嵌套在一个函数的语句序列里。

先看一个普通例子：

```python
# 定义inner函数
def inner():
    print('我是inner')

# 定义outer函数，outer函数调用inner函数
def outer():
    print('我是outer')
    inner()

outer()
# 运行结果：
# 我是outer
# 我是inner
```

改写上面的代码，把`inner`函数写在`outer`函数里面。

```python
# 定义outer函数，outer函数内嵌inner函数，并调用inner函数
def outer():
    print('我是outer')

    # 定义inner函数
    def inner():
        print('我是inner')

    inner()


outer()
# 运行结果：
# 我是outer
# 我是inner
```

上面的外层`outer`函数和内层`inner`函数都没有变量和参数。

现在修改上面的代码，我们传入参数和变量，然后把外层函数返回值指向内层函数名。

```python
def outer():
    a = 1
    print('我是outer')

    # 定义inner函数
    def inner():
        print('我是inner')
        print('inner打印: ', a)
    
    # 返回内层inner函数名
    return inner


f = outer()
# 运行结果：
# 我是outer
f()
# 运行结果：
# 我是inner
# inner打印:  1
```

在上面的例子中：

- `f = outer()`调用外层`outer`函数，并把结果赋值给`f`。注意，inner函数并没有被执行。
- `f`其实就是`inner`，指向`inner`的内存空间。通过`f()`验证了这一点，`outer`函数中的变量`a`被打印出来了。

上面例子中`outer`就是闭包函数，外层函数的变量可以被内层函数调用，类似于封装的效果。内层函数不会立刻被执行，当再次调用时，内层函数才会执行。

闭包函数需要有三个条件：

- 必须有一个内嵌函数，例如函数`inner`；
- 内部函数引用外部函数变量，例如变量`a`；
- 外部函数必须返回内嵌函数，例如`outer`函数中的`return inner`；

对上面的代码再进行修改，在`inner`函数中再添加一个同名的变量a。从结果可以得出结论，`inner`函数优先在内部查找变量`a=5`。

```python
def outer():
    a = 1
    print('我是outer')

    # 定义inner函数
    def inner():
        a = 5
        print('我是inner')
        print('inner打印: ', a)

    return inner


f = outer()
# 运行结果：
# 我是outer
f()
# 运行结果：
# 我是inner
# inner打印:  5
```

结论：内层函数中调用的变量：

- 首先会从内层函数中找，
- 找不到就去外层函数中找，
- 再找不到就到函数外中找，
- 再找不到就到内置的模块中找，
- 再找不到，就报错。

这就是作用域的概念。

继续修改上面的代码，在`inner`函数中修改`outer`函数中变量`a`的值，运行结果报错。结论：内层函数不能修改外层函数的变量值。

```python
def outer():
    a = 1
    print('我是outer')

    # 定义inner函数
    def inner():
        a += 5
        print('我是inner')
        print('inner打印: ', a)

    return inner


f = outer()
# 运行结果：
# 我是outer
f()
# 运行结果：
# UnboundLocalError: local variable 'a' referenced before assignment
```

修正上面的代码。在`inner`函数中对变量a添加一个`nonlocal`的声明，就可以在`inner`函数中修改外层outer函数的变量`a`的值。

```python
def outer():
    a = 1
    print('我是outer')

    # 定义inner函数
    def inner():
        nonlocal a
        a += 5
        print('我是inner')
        print('inner打印: ', a)

    return inner


f = outer()
# 运行结果：
# 我是outer
f()
# 运行结果：
# 我是inner
# inner打印:  6
```

下面这段代码是阶乘（factorial）递归函数的两个不同的定义。

- 第一个定义使用了嵌套的辅助函数`recurse`来对所需要的参数进行递归；这里的`factorial`函数就是闭包函数。
  - 第一步：第一次调用`factorial()`函数，即`n=5`；
  - 第二步：第一次调用内层函数`recurse()`，但不会立刻被执行；
  - 第三步，执行`return recurse(5, 1)`，对参数`product`初始化赋值`1`
  - 第四步：执行`return recurse(5, 5 * 1)`，此时`n=5`，`product=1`。
  - 第五步：执行`return recurse(4, 4 * 5)`，此时`n=4`，`product=5`。
  - 第六步：执行`return recurse(3, 3 * 20)`，此时`n=3`，`product=20`。
  - 第七步：执行`return recurse(2, 2 * 60)`，此时`n=2`，`product=60`。
  - 第八步：执行`return recurse(1, 1 * 120)`，此时`n=1`，`product=120`。
  - 第九步：此时`n=1`，执行`return product`，即`return 120`，结束。
- 第二个定义则是为第二个参数提供了默认值，从而简化了设计。

```python
# 第一个定义
def factorial(n):
    """返回 n 的阶乘"""

    def recurse(n, product):
        """计算阶乘的帮助器"""
        print(n, product)  # 插入这一句是为了能看清楚每一次递归调用的n和product变化
        if n == 1:
            return product
        else:
            return recurse(n - 1, n * product)
    
    return recurse(n, 1)


f = factorial(5)
# 运行结果
5 1
4 5
3 20
2 60
1 120
```

```python
# 第二个定义
def factorial(n, product=1):
    """返回 n 的阶乘"""
    if n == 1:
        return product
    else:
        return factorial(n - 1, n * product)


print(factorial(5))
# 运行结果
# 120
```

### 5.4.高阶函数

函数本身也是一种独特的数据对象。可以把它们赋给变量、存储在数据结构里、作为参数传递给其他函数以及作为其他函数的值返回。

高阶函数（higher-order function）：它接收另一个函数作为参数，并且以某种方式应用该函数。

Python有两个内置的高阶函数，分别是`map`和`filter`，它们可以用于处理可迭代对象。

- `map`函数会接收另一个函数和一个可迭代对象作为参数，返回另一个可迭代对象。这个函数会把作为参数传递的函数应用在可迭代对象里的每个元素上。简单来说，`map`函数会对可迭代对象里的每个元素进行转换。
- `filter`会接受一个布尔函数和一个可迭代对象作为参数，返回这样一个可迭代对象，它的每一个元素都会被传递给布尔函数，如果这个函数返回True，那么这个元素将被保留在返回的可迭代对象里；否则，这个元素将被删除。简单说，`filter`函数会把所有能够通过检验的元素保留在可迭代对象里。
- `functools.reduce`通过把接收两个参数的函数的结果以及迭代对象的下一个元素再次应用于这个接收两个参数的函数，来把可迭代对象计算成单一的值。


示例：把一个整数列表转换成另一个包含这些整数的字符串形式的列表。

传统方法实现：

```python
oldList = [0, 1, 3, 5, 7, 9]
newList = []

for i in oldList:
    newList.append(str(i))

print(newList)
# ['0', '1', '3', '5', '7', '9']
```

用`map`实现：

```python
oldList = [0, 1, 3, 5, 7, 9]
newList = []

newList = list(map(str, oldList))

print(newList)
# ['0', '1', '3', '5', '7', '9']
```

拓展：把一个整数列表中的正整数转换成另一个包含这些整数的字符串形式的列表。

传统实现：

```python
oldList = [0, 1, 3, 5, 7, 9]
newList = []

for i in oldList:
    if i > 0:
        newList.append((str(i)))

print(newList)
# ['1', '3', '5', '7', '9']
```

使用`filter`实现：

```python
oldList = [0, 1, 3, 5, 7, 9]
newList = []


def isPositive(n):
    if n > 0:
        return True

# 创建一个不包含任何零的可迭代对象
newList = list(filter(isPositive, oldList))
print(newList)
# [1, 3, 5, 7, 9]
```

示例：计算从1到10的乘积并输出结果。

通过`for`循环实现：

```python
result = 1
value = 1

for value in range(1, 11):
    result *= value
    value += 1

print(result)

# 运行结果
# 3628800
```

通过`functools.reduce`循环实现：

```python
import functools

result = functools.reduce(lambda x, y: x * y, range(1, 11))

print(result)
# 3628800
```



### 5.5.lambda与匿名函数

语法格式：

```python
lambda <argument list> : <expression>
```

lambda表达式不能像其他Python函数那样包含一整个语句序列。

拓展：用lambda实现把一个整数列表中的正整数转换成另一个包含这些整数的字符串形式的列表，实际就是通过使用匿名的布尔函数来从整数列表里剔除所有为零的元素。

```python
oldList = [0, 1, 3, 5, 7, 9]
newList = []

newList = list(filter(lambda i: i > 0, oldList))

print(newList)
# [1, 3, 5, 7, 9]
```




## 6.捕获异常

## 7.文件及其操作

## 8.创建类

## 9.编程项目
