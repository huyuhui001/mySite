# 高效Python90条之第14条　用sort方法的key参数来表示复杂的排序逻辑

内置的列表类型提供了名叫`sort`的方法，可以根据多项指标给列表list实例中的元素排序。默认情况下，它会根据元素的自然顺序进行排序。
凡是具备自然顺序的内置类型几乎都可以用`sort`方法排列，比如字符串、整数、元组等内置类型，自然顺序是预定义的。

示例 1：简单排序

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(numbers)  # 输出：[1, 1, 2, 3, 4, 5, 6, 9]

words = ["apple", "banana", "cherry", "date", "fig", "grape"]
words.sort()
print(words)
# 输出：['apple', 'banana', 'cherry', 'date', 'fig', 'grape']
```

对于一般类对象所构成的列表，比如下例的`Person`，是没办法用sort方法排序的，因为`sort`方法发现，排序所需要的特殊方法并没有定义在`Person`类中。

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]
people.sort()
# 输出：TypeError: '<' not supported between instances of 'Person' and 'Person'
```

示例 2：自定义对象排序

如果对象定义了 `__lt__`（小于）、`__le__`（小于等于）、`__eq__`（等于）、`__ne__`（不等于）、`__gt__`（大于）和 `__ge__`（大于等于）等特殊方法，那么这些对象也可以用 `sort` 方法来排列。

```python
from dataclasses import dataclass

# @dataclass 装饰器简化了类的定义，自动生成了 __init__ 和 __repr__ 方法。
@dataclass
class Person:
    name: str
    age: int

    def __lt__(self, other):
        return self.age < other.age

people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]

# 调用列表的 sort 方法对 people 列表进行排序。
# 因为 Person 类定义了 __lt__ 方法，sort 方法会根据 age 属性对 Person 对象进行排序。
people.sort()
print(people)
# 输出：[Person(name='Bob', age=25), Person(name='Alice', age=30), Person(name='Charlie', age=35)]
```

更为常见的情况是，很多对象需要在不同的情况下按照不同的标准排序，此时定义自然排序实际上没有意义。`key` 参数允许我们指定一个函数，该函数将被应用于每个元素，以确定排序的依据。

示例 3：按字符串长度排序

```python
words = ["apple", "banana", "cherry", "date", "fig", "grape"]
words.sort(key=len)
print(words)  # 输出：['fig', 'date', 'apple', 'grape', 'banana', 'cherry']
```

示例 4：按多个条件排序

如果需要按多个条件排序，可以将这些条件放在一个元组中，让 `key` 函数返回这样的元组。

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    height: float

people = [
    Person("Alice", 30, 165.5),
    Person("Alen", 25, 170.0),
    Person("Charlie", 30, 160.0),
    Person("David", 28, 175.0),
]

# 按年龄排序，如果年龄相同，则按身高排序
people.sort(key=lambda p: (p.age, p.height))
print(people) 
# 输出：[Person(name='Alen', age=25, height=170.0), Person(name='David', age=28, height=175.0), Person(name='Charlie', age=30, height=160.0), Person(name='Alice', age=30, height=165.5)]

# 按年龄倒序，如果年龄相同，则按身高倒序
people.sort(key=lambda p: (p.age, p.height), reverse=True)
print(people)
# 输出：[Person(name='Alice', age=30, height=165.5), Person(name='Charlie', age=30, height=160.0), Person(name='David', age=28, height=175.0), Person(name='Alen', age=25, height=170.0)]
```

上例中的元组`(p.age, p.height)`，是把首要指标（也就是`age`）写在前面，把次要指标（也就是`height`）写在后面。

在排序条件中使用元组表示法，是利用了元组的一些特点来进行比较操作。

- 元组是一种不可变的序列，能够存放任意的Python值。
- 两个元组之间是可以比较的，因为这种类型本身已经定义了自然顺序，也就是说，`sort`方法所要求的特殊方法（例如`__lt__`方法）​都已经定义好了。
- 元组在实现这些特殊方法时会依次比较每个位置的那两个对应元素，直到能够确定大小为止。

这种做法有个缺点，就是`key`函数所构造的这个元组只能按同一个排序方向来对比它所表示的各项指标（要是升序，就都得是升序；要是降序，就都得是降序）​。

下面代码实现了`age`按升序排而`height`按降序排的效果。但这有个条件，就是需要支持一元减操作符。`age`和`height`支持一元减操作符，但`name`不支持一元减操作符（`str`类型不支持一元减操作符），

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    height: float

people = [
    Person("Alice", 30, 165.5),
    Person("Alen", 25, 170.0),
    Person("Charlie", 30, 160.0),
    Person("David", 28, 175.0),
]

# 按年龄升序，按身高降序，对height使用了一元减操作符
people.sort(key=lambda p: (p.age, -p.height))
print(people)
# 输出：[Person(name='Alen', age=25, height=170.0), Person(name='David', age=28, height=175.0), Person(name='Alice', age=30, height=165.5), Person(name='Charlie', age=30, height=160.0)]

# 按姓名降序，按身高降序，name不支持一元减操作符
people.sort(key=lambda p: (-p.name, p.height))
# 输出：TypeError: bad operand type for unary -: 'str'
```

示例 5：多次调用 `sort` 方法

当我们在排序时要依据多项指标，且某些指标不支持一元减操作符，可以采用多次调用 `sort` 方法，并在每次调用时分别指定 `key` 函数与 `reverse` 参数。
最次要的指标放在第一轮处理，然后逐步处理更为重要的指标，首要指标放在最后一轮处理。

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    height: float

people = [
    Person("Alice", 30, 165.5),
    Person("Alen", 25, 170.0),
    Person("Charlie", 30, 160.0),
    Person("David", 28, 175.0),
]

# 最次要的指标：按身高降序排序
people.sort(key=lambda p: p.height, reverse=True)
print(people)
# 输出：[Person(name='David', age=28, height=175.0), Person(name='Alen', age=25, height=170.0), Person(name='Alice', age=30, height=165.5), Person(name='Charlie', age=30, height=160.0)]

# 次要的指标：按年龄升序排序
people.sort(key=lambda p: p.age)
print(people)
# 输出：[Person(name='Alen', age=25, height=170.0), Person(name='David', age=28, height=175.0), Person(name='Alice', age=30, height=165.5), Person(name='Charlie', age=30, height=160.0)]

# 首要的指标：按名字升序排序
people.sort(key=lambda p: p.name)
print(people)
# 输出：[Person(name='Alice', age=30, height=165.5), Person(name='Bob', age=25, height=170.0), Person(name='Charlie', age=35, height=160.0), Person(name='David', age=28, height=175.0)]
```

无论有多少项排序指标都可以按照这种思路来实现，而且每项指标可以分别按照各自的方向来排，不用全都是升序或全都是降序。只需要倒着写即可，也就是把最主要的那项排序指标放在最后一轮处理。

尽管这示例4和示例5中的两种思路都能实现同样的效果，但只调用一次`sort`，还是要比多次调用`sort`更为简单。所以，在实现多个指标按不同方向排序时，应该优先考虑让`key`函数返回元组，并对元组中的相应指标取相反数。只有在万不得已的时候，才可以考虑多次调用`sort`方法。

示例 6：性能优化

虽然 `key` 参数非常灵活，但在处理大数据集时，性能可能会受到影响。以下是一些优化建议：

1. 使用内置函数：内置函数（如 `len`、`abs`）通常比自定义函数更快。
2. 使用 `itemgetter` 和 `attrgetter`：这些函数通常比 `lambda` 函数更快。
3. 避免重复计算：如果 `key` 函数的计算成本较高，可以先计算结果并存储在元组中。

```python
from operator import itemgetter, attrgetter
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    height: float

people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
    {"name": "David", "age": 28},
]

# 使用 itemgetter 优化性能
people.sort(key=itemgetter("age"))
print(people)
# 输出：[{'name': 'Bob', 'age': 25}, {'name': 'David', 'age': 28}, {'name': 'Alice', 'age': 30}, {'name': 'Charlie', 'age': 35}]

# 使用 attrgetter 优化性能
people = [
    Person("Alice", 30, 165.5),
    Person("Bob", 25, 170.0),
    Person("Charlie", 35, 160.0),
    Person("David", 28, 175.0),
]

people.sort(key=attrgetter("age"))
print(people)
# 输出：[Person(name='Bob', age=25, height=170.0), Person(name='David', age=28, height=175.0), Person(name='Alice', age=30, height=165.5), Person(name='Charlie', age=35, height=160.0)]
```

要点

- 列表的sort方法可以根据自然顺序给其中的字符串、整数、元组等内置类型的元素进行排序。
- 普通对象如果通过特殊方法定义了自然顺序，那么也可以用sort方法来排列，但这样的对象并不多见。
- 可以把辅助函数传给sort方法的key参数，让sort根据这个函数所返回的值来排列元素顺序，而不是根据元素本身来排列。
- 如果排序时要依据的指标有很多项，可以把它们放在一个元组中，让key函数返回这样的元组。对于支持一元减操作符的类型来说，可以单独给这项指标取反，让排序算法在这项指标上按照相反的方向处理。
- 如果这些指标不支持一元减操作符，可以多次调用sort方法，并在每次调用时分别指定key函数与reverse参数。最次要的指标放在第一轮处理，然后逐步处理更为重要的指标，首要指标放在最后一轮处理。
