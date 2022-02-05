# 第10条　用赋值表达式减少重复代码

赋值表达式（assignment expression）是Python 3.8新引入的语法，它会用到海象操作符（walrusoperator）。


a = b是普通的赋值语句，读作a equals b，而a := b则是赋值表达式，读作a walrus b。
这个符号为什么叫walrus呢？因为把:=顺时针旋转90º之后，冒号就是海象的一双眼睛，等号就是它的一对獠牙。

在Python里面经常要先获取某个值，然后判断它是否非零，如果是就执行某段代码。

```
fresh_fruit = {
    'apple': 10,
    'banana': 8,
	'lemon': 5
}

count = fresh_fruit.get('lemon', 0)

if count:
	print('Stock:', count)
else:
	print('Out of Stock')


Result: 
Stock: 5
```

上面的代码改用海象操作符来写：

```
fresh_fruit = {
    'apple': 10,
    'banana': 8,
	'lemon': 5
}

if count := fresh_fruit.get('lemon', 0):
    print('Stock:', count)
else:
    print('Out of Stock')


Result: 
Stock: 5
```

新代码虽然只省了一行，但读起来却清晰很多，因为这种写法明确体现出count变量只与if块有关。

这个赋值表达式先把:=右边的值赋给左边的count变量，然后对自身求值，也就是把变量的值当成整个表达式的值。

由于表达式紧跟着if，程序会根据它的值是否非零来决定该不该执行if块。
这种先赋值再判断的做法，正是海象操作符想要表达的意思。

下面的例子把赋值表达式放在一对括号里面的，因为我们要在if语句里面把这个表达式的结果跟4这个值相比较。而且，通过使用海象操作符把定义pieces放在if/else分支内，也能让代码变得清晰

```
fresh_fruit = {
    'apple': 10,
    'banana': 8,
	'lemon': 5
}

pieces = 0

if (count := fresh_fruit.get('apple', 2)) > 4:
	pieces = count
	print('Stock:', count)
else:
	pieces = 0
	print('Out of Stock')

```

使用海象操作符结构实现switch/case结构。
```
fresh_fruit = {
    'apple': 10,
    'banana': 8,
	'lemon': 5
}

pieces = 0

if (count := fresh_fruit.get('apple', 2)) > 10:
	pieces = count
elif (count := fresh_fruit.get('banana', 2)) > 8:
	pieces = count
elif (count := fresh_fruit.get('lemon', 2)) > 3:
	pieces = count
else:
	pieces = 0

print(pieces)

Result:
5
```

要点：
* 赋值表达式通过海象操作符（:=）给变量赋值，并且让这个值成为这条表达式的结果，于是，我们可以利用这项特性来缩减代码。
* 如果赋值表达式是大表达式里的一部分，就得用一对括号把它括起来。
* 虽说Python不支持switch/case与do/while结构，但可以利用赋值表达式清晰地模拟出这种逻辑。


## 补充：PEP572: 海象运算符

### 用于 if-else 条件表达式

一般写法：
```
a = 15
if a > 10:
	print('hello, it''s walrus')
```
海象运算符：
```
if a := 15 > 10:
	print('hello, it''s walrus')
```

### 用于 while 循环
常规写法：
```
n = 5
while n:
	print('hello walrus: ', n)
	n = n - 1

Result:
hello walrus:  4
hello walrus:  3
hello walrus:  2
hello walrus:  1
hello walrus:  0
```
海象写法：
```
n = 5
while (n := n - 1) + 1:
	print('hello walrus: ', n)

Result:
hello walrus:  4
hello walrus:  3
hello walrus:  2
hello walrus:  1
hello walrus:  0
```
密码校验常规写法：
```
while True:
	psw = input('input password: ')
	if psw == '123':
		break
```
密码校验海象写法：
```
while (psw := input('input password: ')) != '123':
	continue
```

### 用于列表推导式

计算元素平方根，并保留平方根大于 5 的值：
常规写法：(注意，执行了7次，满足条件的3个数字执行了两遍，第一次执行for后面的if f(i) > 5，第二次执行for前面的f(i))。
```
nums = [16, 36, 49, 64]


def f(x):
    print('run f(x) 1 time: ', x)
    return x ** 0.5


print([f(i) for i in nums if f(i) > 5])

Result: 
run f(x) 1 time:  16
run f(x) 1 time:  36
run f(x) 1 time:  36
run f(x) 1 time:  49
run f(x) 1 time:  49
run f(x) 1 time:  64
run f(x) 1 time:  64
[6.0, 7.0, 8.0]
```
海象写法：（函数只执行了4次，性能优于传统写法）
```
nums = [16, 36, 49, 64]


def f(x):
    print('run f(x) 1 time: ', x)
    return x ** 0.5

print([n for i in nums if(n := f(i)) > 5])

Result:
run f(x) 1 time:  16
run f(x) 1 time:  36
run f(x) 1 time:  49
run f(x) 1 time:  64
[6.0, 7.0, 8.0]
```













