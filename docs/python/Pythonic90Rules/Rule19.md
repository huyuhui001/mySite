# 高效Python90条之第19条　不要把函数返回的多个数值拆分到三个以上的变量中

要点

- 函数可以把多个值合起来通过一个元组返回给调用者，以便利用Python的unpacking机制去拆分。
- 对于函数返回的多个值，可以把普通变量没有捕获到的那些值全都捕获到一个带星号的变量里。
- 把返回的值拆分到四个或四个以上的变量是很容易出错的，所以最好不要那么写，而是应该通过小类或namedtuple实例完成。

Python函数提供了许多能够简化编程工作的特性，其中有些和其他编程语言类似，还有一些是Python独有的。这些特性能够更明确地体现出函数的目标。利用这些特性来消除干扰，并突出调用者的想法，可以使程序里面不再出现那么多难以查找的bug。

在 Python 中，函数可以返回多个值，这些值通常通过元组返回。Python 的解包（unpacking）机制允许我们把这些返回值拆分到多个变量中。然而，当函数返回的值超过三个时，这种解包方式可能会变得复杂且容易出错。为了避免这些问题，建议使用小类或 `namedtuple` 来处理多个返回值。

示例 1：函数返回多个值。

注：Python中，函数可以返回多个值，这些值会自动被打包成一个元组（tuple）。

```python
def get_status(numbers):
    minium = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    return minium, maximum, average


length = [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]
result = get_status(length)
minimum, maximum, average = result

print(f"Minimum: {minimum}, Maximum: {maximum}, Average: {average:.2f}")
# 输出：Minimum: 63, Maximum: 80, Average: 71.30

print(type(result))
# 输出：<class 'tuple'>
```

示例 2：使用带星号的变量捕获多余值。这也是一个推荐方法，在返回多个值的时候，用带星号的表达式接收那些没有被普通变量捕获到的值。

```python
def get_status(numbers):
    minium = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    middle = len(numbers) // 2
    numbers.sort()
    return minium, maximum, average, middle, numbers


length = [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]
result = get_status(length)
minimum, maximum, *rest = result

print(f"Minimum: {minimum}, Maximum: {maximum}, The rest: {rest}")
# 输出：Minimum: 63, Maximum: 80, The rest: [71.3, 5, [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]]

print(type(result))
# 输出：<class 'tuple'>
```

示例 3：使用小类来处理多个返回值。类似 `result.minimum` 这种方式方式有效的避免了上面示例中输出顺序搞错的问题。

```python
class NumberStatus:
    def __init__(self, minimum, maximum, average, middle, sorted_numbers):
        self.minimum = minimum
        self.maximum = maximum
        self.average = average
        self.middle = middle
        self.sorted_numbers = sorted_numbers


def get_status(numbers) -> NumberStatus:
    minium = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    middle = len(numbers) // 2
    sorted_numbers = sorted(numbers)
    return NumberStatus(minium, maximum, average, middle, sorted_numbers)


length = [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]
result = get_status(length)

print(f"Minimum: {result.minimum}, Maximum: {result.maximum}, Average: {result.average:.2f}, Middle index: {result.middle}, Sorted numbers: {result.sorted_numbers}")
# 输出：Minimum: 63, Maximum: 80, Average: 71.30, Middle index: 5, Sorted numbers: [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]

print(type(result))
# 输出：<class '__main__.NumberStatus'>
```

示例 4：使用 `namedtuple`。使用 `namedtuple` 定义了一个名为 `NumberStatus` 的数据结构。

- 使用 `namedtuple`：通过定义一个 `namedtuple` 来封装多个返回值，提高代码的可读性和可维护性。
- 不可变性：`namedtuple` 生成的类是不可变的，适合用于表示不可变的数据结构。

```python
from collections import namedtuple

# 定义一个 namedtuple
NumberStatus = namedtuple("NumberStatus", ["minimum", "maximum", "average", "middle", "sorted_numbers"])


def get_status(numbers):
    minium = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    middle = len(numbers) // 2
    sorted_numbers = sorted(numbers)
    return NumberStatus(minium, maximum, average, middle, sorted_numbers)


length = [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]
result = get_status(length)

print(f"Minimum: {result.minimum}, Maximum: {result.maximum}, Average: {result.average:.2f}, Middle index: {result.middle}, Sorted numbers: {result.sorted_numbers}")
# 输出：Minimum: 63, Maximum: 80, Average: 71.30, Middle index: 5, Sorted numbers: [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]

# 尝试修改 namedtuple 的属性
try:
    result.minimum = 60
except AttributeError as e:
    print(e)
# 输出：can't set attribute

print(type(result))
# 输出：<class '__main__.NumberStatus'>
```

示例 5：使用 `dataclass` 和类型注解。

```python
from dataclasses import dataclass

@dataclass
class NumberStatus:
    minimum: int
    maximum: int
    average: float
    middle: int
    sorted_numbers: list

def get_status(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    middle = len(numbers) // 2
    sorted_numbers = sorted(numbers)
    return NumberStatus(minimum, maximum, average, middle, sorted_numbers)

# 使用数据类
length = [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]
result = get_status(length)

print(f"Minimum: {result.minimum}, Maximum: {result.maximum}, Average: {result.average:.2f}, Middle index: {result.middle}, Sorted numbers: {result.sorted_numbers}")
# 输出：Minimum: 63, Maximum: 80, Average: 71.30, Middle index: 5, Sorted numbers: [63, 65, 67, 68, 70, 72, 74, 76, 78, 80]

print(type(result))
# 输出：<class '__main__.NumberStatus'>
```

对比上述 `dataclass` 和 `namedtuple`：

- 使用 `dataclass` :
      - 更灵活：`dataclass` 支持默认值、类型注解、自定义方法等。
      - 可变性：`dataclass` 生成的类是可变的，可以修改属性值。
- 使用 `namedtuple` :
      - `不可变性：namedtuple` 生成的类是不可变的，适合用于表示不可变的数据结构。
      - `轻量级：namedtuple` 比 `dataclass` 更轻量级，适合简单的数据结构。

回顾一下`@dataclass`装饰器和类型注解。

`@dataclass` 是一个装饰器，用于定义 `NumberStatus` 类，并自动生成下面的方法：

- `__init__`：初始化方法，自动根据类属性生成。
- `__repr__`：返回类的字符串表示形式。
- `__eq__`：比较两个实例是否相等。

类型注解用于在代码中明确指定变量、函数参数和返回值的类型。类型注解本身不会影响代码的运行时行为，但可以被静态类型检查工具（如 mypy）用来检查类型错误，从而提高代码的可读性和可维护性。上例中 `minimum: int` 就是一个类型注解，指定了 `minimum` 属性的类型为 `int`。
