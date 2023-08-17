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














## 4.内置多项集及其操作

多项集collection，指能够包含元素的数据结构。下面是

The collection Module in Python provides different types of containers. A Container is an object that is used to store different objects and provide a way to access the contained objects and iterate over them. Some of the built-in containers are Tuple, List, Dictionary, etc.

Below is the list of different containers provided by the collections module.

- Counters
- OrderedDict
- DefaultDict
- ChainMap
- NamedTuple
- DeQue
- UserDict
- UserList
- UserString

## 5.创建函数

## 6.捕获异常

## 7.文件及其操作

## 8.创建类

## 9.编程项目
