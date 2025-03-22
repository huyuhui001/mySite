# 高效Python90条之第13条　通过带星号的unpacking操作来捕获多个元素，不要用切片

基本的unpacking操作需要提前确定需要拆解的序列的长度。
如下例，`car_ages`列表保存每辆车的车龄，然后按照从大到小的顺序排列好。如果直接通过unpacking操作获取其中最旧的两辆车，那么程序运行时会出现异常。

```python
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
oldest, second_oldest = car_ages_descending # 输出：ValueError: too many values to unpack (expected 2)
```

最容易想到的是通过下标把最旧和第二旧的那两辆车取出来，然后把其余的车放到另一份列表中。但这样做会有几个缺点：

- 下标与切片会让代码看起来很乱。
- 容易出错，用这种办法把序列中的元素分成多个子集合，很容易把下标多写或少写一个位置。

```python
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)

oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others) # 输出：20 19 [15, 9, 8, 7, 6, 4, 1, 0]
```

用unpacking中的星号表达式来处理会更好。

```python
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)

oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others) # 输出：20 19 [15, 9, 8, 7, 6, 4, 1, 0]

*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others) # 输出：0 1 [20, 19, 15, 9, 8, 7, 6, 4]
```

使用带星号的表达式的同时，必须要搭配至少一个普通变量（`*others = car_ages_descending`是错误的）。

对于单层结构来说，同一级里面最多只能出现一次带星号的unpacking（`first, *middle, *others = car_ages_descending`是错误的）。如果要拆解的结构有很多层，那么同一级的不同部分里面可以各自出现带星号的unpacking操作。

```python
car_inventory = { 
    'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
    'Airport': ('Skyline', 'Viper', 'Gremlin'),
    'Westside': ('Camaro', 'Nova', 'El Camino')
    }

((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2)),
 (loc3, (best3, *rest3))) = car_inventory.items()

print(f'Best at {loc1} is {best1}, rest is {rest1}') # 输出：Best at Downtown is Silver Shadow, rest is ['Pinto', 'DMC']
print(f'Best at {loc2} is {best2}, rest is {rest2}') # 输出：Best at Airport is Skyline, rest is ['Viper', 'Gremlin']
print(f'Best at {loc3} is {best3}, rest is {rest3}') # 输出：Best at Westside is Camaro, rest is ['Nova', 'El Camino']
```

星号的表达式总会形成一份列表实例。如果要拆分的序列里已经没有元素留给它了，那么列表就是空白的。

```python
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest) # 输出：1 2 []
```

对迭代器做unpacking操作的好处，主要体现在带星号的用法上面，它使迭代器的拆分值更清晰。我们看下面代码：

```python
# 示例1：对迭代器做unpacking
iterator = iter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
a, b, c, *rest, d = iterator
print("a:", a, "b:", b, "c:", c, "rest:", rest, "d:", d)

# 示例2：对列表做unpacking
iterator = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
a, b, c, *rest, d = iterator
print("a:", a, "b:", b, "c:", c, "rest:", rest, "d:", d)
```

先复习一下概念，列表是可迭代对象，但不是迭代器。可迭代对象（Iterable）与迭代器（Iterator）的区别如下：

- 可迭代对象（Iterable）：
      - 可迭代对象是可以被迭代的对象，例如列表、元组、字典、集合、字符串等。
      - 它们实现了 `__iter__()` 方法，该方法返回一个迭代器。
- 迭代器（Iterator）：
      - 迭代器是一个实现了 `__iter__()` 和 `__next__()` 方法的对象。
      - `__iter__()` 方法返回迭代器本身。
      - `__next__()` 方法返回序列中的下一个值，如果没有更多值，则抛出 `StopIteration` 异常。

上面2个示例的输出都是`a: 1 b: 2 c: 3 rest: [4, 5, 6, 7, 8, 9] d: 10`，但它们是有区别的：

- 数据结构：
      - 示例1：是一个迭代器对象，通过 `iter()` 函数从列表 `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` 创建。
      - 示例2：是一个列表 `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`。
- 内存使用：
      - 示例1：迭代器是惰性的，它不会一次性加载所有数据到内存中。每次调用 `next(iterator)` 时，迭代器才会生成下一个值。这在处理大数据集时可以节省内存。
      - 示例2：列表会一次性加载所有数据到内存中。如果数据集非常大，这可能会占用较多的内存。
- 性能：
      - 示例1：迭代器的解包操作可能比直接从列表中解包稍慢，因为每次从迭代器中提取值都需要调用 `next()`。
      - 示例2：直接从列表中解包操作通常更快，因为列表支持随机访问，可以直接通过索引访问元素。
- 可重用性：
      - 示例1：迭代器是一次性的，一旦被完全消耗（即所有元素都被提取），就不能再次使用。如果需要重新访问数据，需要重新创建迭代器。
      - 示例2：列表可以多次访问，因为它是可重用的数据结构。

要点

- 拆分数据结构并把其中的数据赋给变量时，可以用带星号的表达式，将结构中无法与普通变量相匹配的内容捕获到一份列表里。
- 这种带星号的表达式可以出现在赋值符号左侧的任意位置，它总是会形成一份含有零个或多个值的列表。
- 在把列表拆解成互相不重叠的多个部分时，这种带星号的unpacking方式比较清晰，而通过下标与切片来实现的方式则很容易出错。
