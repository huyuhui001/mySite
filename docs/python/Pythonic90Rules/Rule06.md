# 第6条　把数据结构直接拆分到多个变量里，不要专门通过下标访问

Python内置的元组（tuple）类型可以创建不可变的序列，把许多元素依次保存起来。 可以用整数作下标，通过下标来访问元组里面对应的元素。但不能通过下标给元素赋新值。

```
>>> snack_calories = {
...     'chips': 140,
...     'popcorn': 80,
...     'nuts': 190
... }

>>> items = tuple(snack_calories.items())

>>> type(snack_calories)
<class 'dict'>
>>> type(items)
<class 'tuple'>

>>> snack_calories
{'chips': 140, 'popcorn': 80, 'nuts': 190}
>>> items
(('chips', 140), ('popcorn', 80), ('nuts', 190))

>>> items[2]
('nuts', 190)

>>> items[1] = ('apple', 200)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

Python还有一种写法，叫作拆分（unpacking）。这种写法让我们只用一条语句，就可以把元组里面的元素分别赋给多个变量，不用再通过下标去访问。 元组的元素本身不能修改，但是那些被赋值的变量是可以修改的。
通过unpacking来赋值要比通过下标去访问元组内的元素更清晰，而且这种写法所需的代码量通常比较少。当然，赋值操作的左边除了可以罗列单个变量，也可以写成列表、序列或任意深度的可迭代对象（iterable）。

```
>>> favorite_snacks = {
...     'salty': ('pretzels', 100),
...     'sweet': ('cookies', 280),
...     'veggie': ('carrots', 20)
... }

>>> (
...     (type1, (name1, cals1)),
...     (type2, (name2, cals2)),
...     (type3, (name3, cals3)),
... ) = favorite_snacks.items()

>>> print(f'Favorite {type1} is {name1} with {cals1} calories')
Favorite salty is pretzels with 100 calories

>>> print(f'Favorite {type2} is {name2} with {cals2} calories')
Favorite sweet is cookies with 280 calories

>>> print(f'Favorite {type3} is {name3} with {cals3} calories')
Favorite veggie is carrots with 20 calories
```

可以通过unpacking原地交换两个变量，而不用专门创建临时变量。

```
>>> def bubble_sort(a):
...     for _ in range(len(a)):
...         for i in range(1, len(a)):
...             if a[i] < a[i - 1]:
...                 temp = a[i]
...                 a[i] = a[i - 1]
...                 a[i - 1] = temp
... 
>>> names = ['pretzels', 'carrots', 'arugula', 'bacon']
>>> bubble_sort(names)
>>> names
['arugula', 'bacon', 'carrots', 'pretzels']
```

```
>>> def bubble_sort(a):
...     for _ in range(len(a)):
...         for i in range(1, len(a)):
...             if a[i] < a[i - 1]:
...                 a[i], a[i - 1] = a[i - 1], a[i]
... 
>>> names = ['pretzels', 'carrots', 'arugula', 'bacon']
>>> bubble_sort(names)
>>> names
['arugula', 'bacon', 'carrots', 'pretzels']
```

原理分析：

Python处理赋值操作的时候，要先对=号右侧求值，于是，它会新建一个临时的元组，把`a[i]`与`a[i-1]`这两个元素放到这个元组里面。例如，第一次进入内部的for循环时，这两个元素分别是`'carrots'`与`'pretzels`'，于是，系统就会创建出`('carrots','pretzels')`这样一个临时的元组。

然后，Python会对这个临时的元组做unpacking，把它里面的两个元素分别放到=号左侧的那两个地方，于是，`'carrots'`就会把`a[i-1]`里面原有的`'pretzels'`换掉，`'pretzels'`也会把`a[i]`里面原有的`'carrots'`换掉。

现在，出现在`a[0]`这个位置上面的字符串就是`'carrots'`了，出现在`a[1]`这个位置上面的字符串则是`'pretzels'`。

做完unpacking后，系统会扔掉这个临时的元组。

unpacking机制还有一个特别重要的用法，就是可以在for循环或者类似的结构里面，把复杂的数据拆分到相关的变量之中。

```
>>> snacks = [('bacon', 350), ('donut', 240), ('muffin', 190)]
>>> for i in range(len(snacks)):
...     item = snacks[i]
...     name = item[0]
...     calories = item[1]
...     print(f'#{i+1}: {name} has {calories} calories')
... 
#1: bacon has 350 calories
#2: donut has 240 calories
#3: muffin has 190 calories
```

上面这段代码虽然没错，但看起来很乱，因为snacks结构本身并不是一份简单的列表，它的每个元素都是一个元组， 所以必须逐层访问才能查到最为具体的数据，也就是每种零食的名称（name）及卡路里（calories）。

下面换一种写法，首先调用内置的enumerate函数（参见第7条）获得当前要迭代的元组， 然后针对这个元组做unpacking，这样就可以直接得到具体的name与calories值了。

这才是符合Python风格的写法（Pythonic式的写法）。

```
>>> for rank, (name, calories) in enumerate(snacks, 1):
...     print(f'#{rank}: {name} has {calories} calories')
... 
#1: bacon has 350 calories
#2: donut has 240 calories
#3: muffin has 190 calories
```

Python的unpacking机制可以用在许多方面，例如构建列表（Rule13）、给函数设计参数列表（Rule22）、传递关键字参数（Rule23）、接收多个返回值（Rule19条）等。

要点：

* unpacking是一种特殊的Python语法，只需要一行代码，就能把数据结构里面的多个值分别赋给相应的变量。
* unpacking在Python中应用广泛，凡是可迭代的对象都能拆分，无论它里面还有多少层迭代结构。
* 尽量通过unpacking来拆解序列之中的数据，而不要通过下标访问，这样可以让代码更简洁、更清晰。

## 拓展：Packing and Unpacking in Python

Python allows a tuple (or list) of variables to appear on the left side of an assignment operation.

Each variable in the tuple can receive one value (or more, if we use the * operator) from an iterable on the right side
of the assignment. Unpacking in Python refers to an operation that consists of assigning an iterable of values to a
tuple (or list) of variables in a single assignment statement.

In Python, we can put a tuple of variables on the left side of an assignment operator (=) and a tuple of values on the
right side. The values on the right will be automatically assigned to the variables on the left according to their
position in the tuple. This is commonly known as tuple unpacking in Python. Check out the following example:

```
>>> (a, b, c) = (1, 2, 3)
>>> a
1
>>> b
2
>>> c
3
>>> birthday = ('April', 5, 2001)
>>> month, day, year = birthday
>>> month
'April'
>>> day
5
>>> year
2001
```

The tuple unpacking feature got so popular among Python developers that the syntax was extended to work with any
iterable object. The only requirement is that the iterable yields exactly one item per variable in the receiving tuple (
or list).

Check out the following examples of how iterable unpacking works in Python:

```
>>> # Unpackage strings
>>> a, b, c = '123'
>>> a
'1'
>>> b
'2'
>>> c
'3'
>>> # Unpackaging strings
>>> a, b, c = '123'
>>> a
'1'
>>> b
'2'
>>> c
'3'
>>> # Unpacking lists
>>> a, b, c = [1, 2, 3]
>>> a
1
>>> b
2
>>> c
3
>>> # Unpacking generators
>>> gen = (i ** 2 for i in range(3))
>>> a, b, c = gen
>>> a
0
>>> b
1
>>> c
4
>>> # Upacking dictionaries (keys, values, and items)
>>> my_dict = {'one': 1, 'two': 2, 'three': 3}
>>> a, b, c = my_dict
>>> a
'one'
>>> b
'two'
>>> c
'three'
>>> a, b, c = my_dict.values()
>>> a
1
>>> b
2
>>> c
3
>>> a, b, c = my_dict.items()
>>> a
('one', 1)
>>> b
('two', 2)
>>> c
('three', 3)
>>> # Use a tuple on the right side of assignment statement
>>> [a, b, c] = 1, 2, 3
>>> a
1
>>> b
2
>>> c
3
>>> # Use range() iterator
>>> x, y, z = range(3)
>>> x
0
>>> y
1
>>> z
2
```

As a complement, the term packing can be used when we collect several values in a single variable using the iterable
unpacking operator.

The * operator is known, in this context, as the tuple (or iterable) unpacking operator. It extends the unpacking
functionality to allow us to collect or pack multiple values in a single variable.

In the following example, we pack a tuple of values into a single variable by using the * operator:

```
>>> *a, = 1, 2
>>> a
[1, 2]
```

For this code to work, the left side of the assignment must be a tuple (or a list). That's why we use a trailing comma.
This tuple can contain as many variables as we need. However, it can only contain one starred expression.

```
>>> # Packing trailing values
>>> a, *b = 1, 2, 3
>>> a
1
>>> b
[2, 3]
>>> *a, b, c = 1, 2, 3
>>> a
[1]
>>> b
2
>>> c
3
>>> *a, b, c, d, e = 1, 2, 3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: not enough values to unpack (expected at least 4, got 3)
>>> *a, b, c, d = 1, 2, 3
>>> a
[]
>>> b
1
>>> c
2
>>> d
3
>>> 
>>> seq = [1, 2, 3, 4]
>>> first, *body, last = seq
>>> first, body, last
(1, [2, 3], 4)
>>> first, body, *last = seq
>>> first, body, last
(1, 2, [3, 4])
>>> ran = range(10)
>>> *r, = ran
>>> r
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Using Packing and Unpacking in Practice

```
>>> employee = ['John Doe', '40', 'Software Engineer']
>>> name = employee[0]
>>> age = employee[1]
>>> job = employee[2]
>>> name
'John Doe'
>>> age
'40'
>>> job
'Software Engineer'
>>> 
>>> name, age, job = ['John Doe', '40', 'Software Engineer']
>>> name
'John Doe'
>>> age
'40'
>>> job
'Software Engineer'
>>> 
>>> a = 100
>>> b = 200
>>> a, b = b, a
>>> a
200
>>> b
100
```

Dropping Unneeded Values With *

```
>>> a, b, *_ = 1, 2, 0, 0, 0, 0
>>> a
1
>>> b
2
>>> _
[0, 0, 0, 0]

```

The rest of the information is stored in the dummy variable _, which can be ignored by our program.

By default, the underscore character _ is used by the Python interpreter to store the resulting value of the statements
we run in an interactive session. So, in this context, the use of this character to identify dummy variables can be
ambiguous.

Returning Tuples in Functions

```
>>> def powers(num):
...     return num, num ** 2, num ** 3
... 
>>> # Packaging returned values in a tuple
>>> result = powers(3)
>>> result
(3, 9, 27)
>>> # Unpacking returned values to multiple variables
>>> number, square, cube = powers(3)
>>> number
3
>>> square
9
>>> cube
27
>>> *_, cube = powers(3)
>>> cube
27
```

Merging Iterables With the * Operator The last two examples show that this is also a more readable and efficient way to
concatenate iterables. Instead of writing list(my_set) + my_list + list(my_tuple) + list(range(1, 4)) + list(my_str) we
just write `[*my_set, *my_list, *my_tuple, *range(1, 4), *my_str]`.

```
>>> my_tuple = (1, 2, 3)
>>> (0, *my_tuple, 4)
(0, 1, 2, 3, 4)
>>> my_list = [1, 2, 3]
>>> [0, *my_list, 4]
[0, 1, 2, 3, 4]
>>> my_set = {1, 2, 3}
>>> {0, *my_set, 4}
{0, 1, 2, 3, 4}
>>> [*my_set, *my_list, *my_tuple, *range(1, 4)]
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> my_str = "123"
>>> [*my_set, *my_list, *my_tuple, *range(1, 4), *my_str]
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, '1', '2', '3']

```

Unpacking Dictionaries With the ** Operator

```
>>> numbers = {'one': 1, 'two': 2, 'three': 3}
>>> letters = {'a': 'A', 'b': 'B', 'c': 'C'}
>>> combination = {**numbers, **letters}
>>> combination
{'one': 1, 'two': 2, 'three': 3, 'a': 'A', 'b': 'B', 'c': 'C'}
```

An important point to note is that, if the dictionaries we're trying to merge have repeated or common keys, then the
values of the right-most dictionary will override the values of the left-most dictionary. Here's an example:

```
>>> letters = {'a': 'A', 'b': 'B', 'c': 'C'}
>>> vowels = {'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u'}
>>> {**letters, **vowels}
{'a': 'a', 'b': 'B', 'c': 'C', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u'}
>>> {**vowels, **letters}
{'a': 'A', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u', 'b': 'B', 'c': 'C'}
```

Unpacking in For-Loops

We can also use iterable unpacking in the context of for loops. When we run a for loop, the loop assigns one item of its
iterable to the target variable in every iteration. If the item to be assigned is an iterable, then we can use a tuple
of target variables. The loop will unpack the iterable at hand into the tuple of target variables.

We can build a list of two-elements tuples. Each tuple will contain the name of the product, the price, and the sold
units. With this information, we want to calculate the income of each product. To do this, we can use a for loop like
this:

```
>>> sales = [('Pencle', 0.22, 1500), ('Notebook', 1.30, 550), ('Eraser', 0.75, 1000)]
>>> for items in sales:
...     print(f"Income for {item[0]} is: {item[1] * item[2]}")
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'item' is not defined
>>> for items in sales:
...     print(f"Income for {items[0]} is: {items[1] * items[2]}")
... 
Income for Pencle is: 330.0
Income for Notebook is: 715.0
Income for Eraser is: 750.0
```

we're using indices to get access to individual elements of each tuple. This can be difficult to read and to understand
by newcomer developers. We're now using iterable unpacking in our for loop in below sample codes, which is an
alternative implementation using unpacking in Python:

```
>>> sales = [('Pencle', 0.22, 1500), ('Notebook', 1.30, 550), ('Eraser', 0.75, 1000)]
>>> for product, price, sold_units in sales:
...     print(f"Income for {product} is: {price * sold_units}")
... 
Income for Pencle is: 330.0
Income for Notebook is: 715.0
Income for Eraser is: 750.0
```

It's also possible to use the * operator in a for loop to pack several items in a single target variable. In this for
loop, we're catching the first element of each sequence in first. Then the * operator catches a list of values in its
target variable rest.

```
>>> for first, *rest in [(1, 2, 3),(4, 5, 6)]:
...     print('First: ', first)
...     print('Rest: ', rest)
... 
First:  1
Rest:  [2, 3]
First:  4
Rest:  [5, 6]
>>> 
```

Finally, the structure of the target variables must agree with the structure of the iterable. Otherwise, we'll get an
error. Take a look at the following example:

```
>>> data = [((1, 2), 3), ((2, 3), 3)]
>>> for (a, b), c in data:
...     print(a, b, c)
... 
1 2 3
2 3 3
>>> for a, b, c in data:
...     print(a, b, c)
... 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: not enough values to unpack (expected 3, got 2)
```

Defining Functions With * and **

The below function requires at least one argument called `required`. It can accept a variable number of positional and
keyword arguments as well. In this case, the * operator *collects or packs* extra positional arguments in a tuple called
`args` and the ** operator collects or packs extra keyword arguments in a dictionary called `kwargs`. Both, `args`
and `kwargs`, are optional and automatically default to () and {} respectively.

Even though the names `args` and `kwargs` are widely used by the Python community, they're not a requirement for these
techniques to work. The syntax just requires * or ** followed by a valid identifier. So, if you can give meaningful
names to these arguments, then do it. That will certainly improve your code's readability.

```
>>> def func(required, *args, **kwargs):
...     print(required)
...     print(args)
...     print(kwargs)
... 
>>> func('Welcome to ...', 1, 2, 3, site='CloudAcademy.com')
Welcome to ...
(1, 2, 3)
{'site': 'CloudAcademy.com'}
>>> func('Welcome to ...', 1, 2, 3, 4)
Welcome to ...
(1, 2, 3, 4)
{}
>>> func('Welcome to ...', 1, 2, 3, (1, 2))
Welcome to ...
(1, 2, 3, (1, 2))
{}
>>> func('Welcome to ...', 1, 2, 3, [1, 2])
Welcome to ...
(1, 2, 3, [1, 2])
{}
>>> func('Welcome to ...', 1, 2, 3, ([2, 3], [1, 2]))
Welcome to ...
(1, 2, 3, ([2, 3], [1, 2]))
{}
```

Calling Functions With * and **

When calling functions, we can also benefit from the use of the * and ** operator to unpack collections of arguments
into separate positional or keyword arguments respectively. This is the inverse of using * and ** in the signature of a
function. In the signature, the operators mean collect or pack a variable number of arguments in one identifier. In the
call, they mean *unpack* an iterable into several arguments.

Here's a basic example of how this works. The * operator unpacks sequences like `["Welcome", "to"]` into positional
arguments. Similarly, the ** operator unpacks dictionaries into arguments whose names match the keys of the unpacked
dictionary.

```
>>> def func(welcome, to, site):
...     print(welcome, to, site
... 
... )
... 
>>> def func(welcome, to, site):
...     print(welcome, to, site)
... 
>>> func(*['Welcome', 'to'], **{'site': 'CloudAcademy.com'})
Welcome to CloudAcademy.com

```

We can also combine this technique and the one covered in the previous section to write quite flexible functions. The
use of the * and ** operators, when defining and calling Python functions, will give them extra capabilities and make
them more flexible and powerful.

Here's an example:

```
>>> def func(required, *args, **kwargs):
...     print(required)
...     print(args)
...     print(kwargs)
... 
>>> func('Welcome to...', *(1, 2, 3), **{'Site': 'CloudAcademy.com'})
Welcome to...
(1, 2, 3)
{'Site': 'CloudAcademy.com'}
```

Conclusion

Iterable unpacking turns out to be a pretty useful and popular feature in Python. This feature allows us to unpack an
iterable into several variables. On the other hand, packing consists of catching several values into one variable using
the unpacking operator, *.

In this tutorial, we've learned how to use iterable unpacking in Python to write more readable, maintainable, and
pythonic code.

With this knowledge, we are now able to use iterable unpacking in Python to solve common problems like parallel
assignment and swapping values between variables. We're also able to use this Python feature in other structures like
for loops, function calls, and function definitions.

## 拓展：enumerate

enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

enumerate() 方法:
语法

* `enumerate(sequence, [start=0])`

参数

* sequence：一个序列、迭代器或其他支持迭代对象。
* start：下标起始位置。 返回值

返回

* enumerate(枚举) 对象。

基本用法：

* 字符串

```
>>> sample = 'abcd'
>>> for i, j in enumerate(sample):  # 输出的是元组内的元素
...     print(i, j)
... 
0 a
1 b
2 c
3 d

>>> for i in enumerate(sample):  # 输出的是元组
...     print(i)
... 
(0, 'a')
(1, 'b')
(2, 'c')
(3, 'd')

>>> sample = ('abcd')
>>> for i, j in enumerate(sample):
...     print(i, j)
... 
0 a
1 b
2 c
3 d
```

* 元组

```
>>> sample = ('abcd', 'hijk')
>>> for i, j in enumerate(sample):
...     print(i, j)
... 
0 abcd
1 hijk

>>> sample = ('abcd', 'hijk')
>>> for i, j in enumerate(sample, 2):
...     print(i, j)
... 
2 abcd
3 hijk
```

* 数组

```
>>> sample = ['abcd', 'hijk']
>>> for i, j in enumerate(sample):
...     print(i, j)
... 
0 abcd
1 hijk
```

* 字典

```
>>> sample = {'abcd': 1, 'hijk': 2}
>>> for i, j in enumerate(sample):
...     print(i, j)
... 
0 abcd
1 hijk
```




