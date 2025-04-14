# 高效Python90条之第22条　用数量可变的位置参数给函数设计清晰的参数列表

要点

- 用`def`定义函数时，可以通过`*args`的写法让函数接受数量可变的位置参数。
- 调用函数时，可以在序列左边加上`*`操作符，把其中的元素当成位置参数传给`*args`所表示的这一部分。
- 如果`*`操作符加在生成器前，那么传递参数时，程序有可能因为耗尽内存而崩溃。给接受`*args`的函数添加新位置参数，可能导致难以排查的bug。

示例 1：基本用法，使用 `*args` 接受数量可变的位置参数。

在函数定义中，`*args` 用于捕获所有未命名的位置参数，并将它们存储在一个元组中。在调用函数时，在序列左边加上 `*` 操作符，将序列中的元素作为位置参数传递给 `*args`。

```python
def print_args(*args):
    for arg in args:
        print(arg)

print_args(1, 2, 3, "hello", [1, 2, 3])
# 输出:
# 1
# 2
# 3
# hello
# [1, 2, 3]
```

示例 2：调用函数时使用 `*` 操作符。

在调用函数时，`*args` 将序列中的元素作为位置参数传递给函数。

```python
def print_args(*args):
    for arg in args:
        print(arg)

args = [1, 2, 3, "hello", [1, 2, 3]]
print_args(*args)
# 输出:
# 1
# 2
# 3
# hello
# [1, 2, 3]
```

如果 `*` 操作符加在生成器前，可能会导致程序耗尽内存而崩溃，因为生成器在传递参数时会生成所有值，而不是按需生成。

示例 3：生成器导致内存耗尽。

生成器按需生成值，而不是一次性生成所有值。如果在传递参数时耗尽内存，程序可能会崩溃。

```python
def print_args(*args):
    for arg in args:
        print(arg)

# 生成器
gen = (i for i in range(1000000000))

# 这可能会耗尽内存
try:
    print_args(*gen)
except MemoryError as e:
    print("MemoryError:", e)
# 输出:
# 当前系统是Ubuntu 24.04，物理内存是64G，程序运行是物理内存最高水位达到98%，然后系统开始输入print结果。
```

示例 4：添加新位置参数引起的问题。

给接受 `*args` 的函数添加新位置参数`a`，导致意料外的问题，在复杂情况下，排错成本很高。

```python
def print_args(a, *args):
    for arg in args:
        print(arg)

# 调用函数时，调用者可能没有意识到新的参数被添加了
args = [1, 2, 3, "hello", [1, 2, 3]]
print_args(*args)
# 输出:
# 2
# 3
# hello
# [1, 2, 3]
```

示例 5：`*args`与关键字参数结合使用，提供更灵活的函数接口。

`**kwargs` 用于捕获所有未命名的关键字参数，并将它们存储在一个字典中。

```python
def print_args(*args, **kwargs):
    a="new"
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key}: {value}")

args = [1, 2, 3, "hello", [1, 2, 3]]
kwargs = {"name": "Alice", "age": 30}

print_args(*args)
# 输出:
# 1
# 2
# 3
# hello
# [1, 2, 3]
print_args(**kwargs)
# 输出:
# name: Alice
# age: 30
```

示例 6：使用 `functools.partial`可以用于固定某些参数，使函数接口更加灵活。

```python
import functools


def print_args(a, *args, **kwargs):
    print("First argument:", a)
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key}: {value}")


# 固定第一个参数
partial_print_args = functools.partial(print_args, "new")

args = [1, 2, 3, "hello", [1, 2, 3]]
kwargs = {"name": "Alice", "age": 30}

print_args(*args)  # 这里的a参数的值是1
# 输出:
# First argument: 1
# 2
# 3
# hello
# [1, 2, 3]

print_args(**kwargs)
# 输出:
# TypeError: print_args() missing 1 required positional argument: 'a'

partial_print_args(*args) # 这里的a参数的值是new
# 输出:
# First argument: new
# 1
# 2
# 3
# hello
# [1, 2, 3]

partial_print_args(**kwargs) # 这里的a参数的值是new
# 输出:
# First argument: new
# name: Alice
# age: 30
```
