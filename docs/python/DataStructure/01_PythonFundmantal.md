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

## 3.字符串及其运算

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
