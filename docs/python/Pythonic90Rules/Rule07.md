# 第7条　尽量用enumerate取代range

Python内置的range函数适合用来迭代一系列整数。

```
>>> from random import randint
>>> random_bits = 0
>>> for i in range(32):
...     if randint(0, 1):
...         random_bits |= 1 << i  # 运算符|是二进制OR操作
... 
>>> print(bin(random_bits))
0b110110000110100101001011010
```

如果要迭代的是某种数据结构，例如字符串列表，那么可以直接在这个序列上面迭代，不需要通过range。

```
>>> flavor_list第8条　用zip函数同时遍历两个迭代器 = ['vanilla', 'chocolate', 'pecan', 'strawberry']
>>> for flavor in flavor_list:
...     print(f'{flavor} is delicious')
... 
vanilla is delicious
chocolate is delicious
pecan is delicious
strawberry is delicious
```

通过传统的range方法，给每种口味添加序列号。但步骤有些太多，先得知道列表的长度，然后要根据列表长度构造取值范围，用其中的每个整数做下标，分别访问列表里的对应元素。

```
>>> for i in range(len(flavor_list)):
...     flavor = flavor_list[i]
...     print(f'{i + 1}: {flavor}')
... 
1: vanilla
2: chocolate
3: pecan
4: strawberry
```

Python的内置的函数enumerate，能够把任何一种迭代器（iterator）封装成惰性生成器（lazy generator，参见Rule30）。
这样每次循环的时候，它只需要从iterator里面获取下一个值就行了，同时还会给出本轮循环的序号，即生成器每次产生的一对输出值。

下面通过内置的next函数手动推进enumerate所返回的这个iterator，来演示enumerate。

```
>>> it = enumerate(flavor_list)
>>> print(next(it))
(0, 'vanilla')
>>> print(next(it))
(1, 'chocolate')
>>> print(next(it))
(2, 'pecan')
>>> print(next(it))
(3, 'strawberry')
>>> print(next(it))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

enumerate输出的每一对数据，都可以拆分（unpacking）到for语句的那两个变量里面（unpacking机制参见Rule06），这样会让代码更加清晰。

```
>>> for i, flavor in enumerate(flavor_list):
...     print(f'{i + 1}: {flavor}')
... 
1: vanilla
2: chocolate
3: pecan
4: strawberry

>>> for i, flavor in enumerate(flavor_list, 1):
...     print(f'{i}: {flavor}')
... 
1: vanilla
2: chocolate
3: pecan
4: strawberry
```

要点：

* enumerate函数可以用简洁的代码迭代iterator，而且可以指出当前这轮循环的序号。
* 不要先通过range指定下标的取值范围，然后用下标去访问序列，而是应该直接用enumerate函数迭代。
* 可以通过enumerate的第二个参数指定起始序号（默认为0）。














