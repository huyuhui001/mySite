# 第9条　不要在for与while循环后面写else块

Python的循环有一项大多数编程语言都不支持的特性，即可以把else块紧跟在整个循环结构的后面。
程序做完整个for循环之后，竟然会执行else块里的内容。

```
>>> for i in range(3):
...     print('loop', i)
... else:
...     print('Else block!')
...
loop 0
loop 1
loop 2
Else block!
```

try/except/else结构里的else（参见Rule65条），它的意思是：如果没有异常需要处理，那就执行这块语句。

try/finally结构里的finally，它的意思是：不管前面那块代码执行得如何，最后都要执行finally块代码。

for/else结构里面的else，它的意思是：如果循环没有从头到尾执行完（也就是循环提前终止了），那么else块里的代码是不会执行的。在循环中使用break语句实际上会跳过else块。

```
>>> for i in range(3):
...     print('loop', i)
...     if i == 1:
...         break
... else:
...     print('Else block!')
...
loop 0
loop 1
```

还有一个奇怪的地方是，如果对空白序列做for循环，那么程序立刻就会执行else块。

```
>>> for x in []:
...     print('Never Runs')
... else:
...     print('For Else block!')
...
For Else block!
```

while循环也是这样，如果首次循环就遇到False，那么程序也会立刻运行else块。

```
>>> while True:
...     print('Never runs')
...     break
... else:
...     print('While Else block!')
...
Never runs

>>> while False:
...     print('Never runs')
... else:
...     print('While Else block!')
...
While Else block!
```

Python把else设计成这样，主要目的是利用它实现搜索逻辑。

例如下面代码，如果要判断两个数是否互质（也就是除了1之外，是不是没有别的数能够同时整除它们），就可以用这种结构实现。
先把有可能同时整除它们的数逐个试一遍，如果全都试过之后还是没找到这样的数，
那么循环就会从头到尾执行完（这意味着循环没有因为break而提前跳出），
然后程序就会执行else块里的代码。

```
>>> for i in range(2, min(a, b) + 1):
...     print('Testing', i)
...     if a % i == 0 and b% i == 0:
...             print('Not coprime')
... else:
...     print('Coprime')
...
Testing 2
Testing 3
Testing 4
Coprime

```

实际工作中，上述代码会改用辅助函数完成。这样的辅助函数有两种常见的写法。


第一种写法是，只要发现某个条件成立，就立刻返回，如果始终都没碰到这种情况，那么循环就会完整地执行，让程序返回函数末尾的那个值作为默认返回值。
```
>>> def coprime(a, b):
...     for i in range(2, min(a, b) + 1):
...         if a % i == 0 and b% i == 0:
...             return False
...     return True
...
>>> assert coprime(4, 9)

>>> assert not coprime(4, 9)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

>>> assert coprime(3, 6)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

>>> assert not coprime(3, 6)
>>>
```

第二种写法是，用变量来记录循环过程中有没有碰到这样的情况，如果有，那就用break提前跳出循环，如果没有，循环就会完整地执行，无论如何，最后都返回这个变量的值。
```
>>> def coprime_alternate(a, b):
...     is_coprime = True
...     for i in range(2, min(a, b) + 1):
...         if a % i == 0 and b% i == 0:
...             is_coprime = False
...             break
...     return is_coprime
...
>>> assert coprime_alternate(4, 9)

>>> assert not coprime_alternate(4, 9)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

>>> assert coprime_alternate(3, 6)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

>>> assert not coprime_alternate(3, 6)
>>>
```

对于不熟悉for/else结构的人来说，刚才那两种写法都是比较清晰的方案。

for/else或while/else结构本身虽然可以实现某些逻辑表达，但它带来的困惑已经盖过了它的好处，会让代码产生歧义。所以，请不要这么写。

要点：
* Python有种特殊的语法，可以把else块紧跟在整个for循环或while循环的后面。
* 只有在整个循环没有因为break提前跳出的情况下，else块才会执行。
* 把else块紧跟在整个循环后面，会让人不太容易看出这段代码的意思，所以要避免这样写。







