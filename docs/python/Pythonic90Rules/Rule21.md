# 高效Python90条之第21条　了解如何在闭包里面使用外围作用域中的变量

要点

- 闭包函数可以引用定义它们的那个外围作用域之中的变量。
- 按照默认的写法，在闭包里面给变量赋值并不会改变外围作用域中的同名变量。
- 先用`nonlocal`语句说明，然后赋值，可以修改外围作用域中的变量。除特别简单的函数外，尽量少用`nonlocal`语句。

Python中的闭包(closure)是一种函数式编程特性，闭包函数能够访问定义它们的外围作用域中的变量，这是其核心特性。

在下面这个例子中，`inner_function`是一个闭包，它能够访问外围函数`outer_function`的局部变量`message`，即使`outer_function`已经执行完毕。

```python
def outer_function():
    message = "Hello"
    
    def inner_function():
        print(message)  # 访问外围作用域的变量
        
    return inner_function

closure = outer_function()
closure()
# 输出: Hello
```

默认情况下，在闭包中对变量赋值会在闭包的局部作用域中创建一个新变量，而不是修改外围作用域中的同名变量。这是因为Python在编译函数时，会将所有赋值语句左边的变量默认为局部变量。

在下面的例子中，当`increment`尝试对`count`赋值时，Python认为`count`是局部变量，但在执行`count += 1`时发现它还没有被初始化，因此抛出错误。

```python
def counter():
    count = 0
    
    def increment():
        count += 1  # 这会导致 UnboundLocalError
        return count
        
    return increment

c = counter()
c()
# 输出: UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
```

要修改外围作用域中的变量，可以使用`nonlocal`声明。对上面的示例代码可以使用`nonlocal`来解决`UnboundLocalError`的错误。`nonlocal`语句告诉Python解释器，`count`变量不是局部的，而是来自外围作用域。

```python
def counter():
    count = 0
    
    def increment():
        nonlocal count  # 声明count来自外围作用域
        count += 1
        return count
        
    return increment

c = counter()
print(c())  # 输出: 1
print(c())  # 输出: 2
print(c())  # 输出: 3
```

在实际应用中，闭包常用于创建有状态的装饰器。

下面是一个记录函数调用次数的装饰器实现，这个装饰器利用闭包和`nonlocal`变量来保持调用计数状态，而不需要使用类或全局变量。

```python
def call_counter(func):
    count = 0
    
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"Function {func.__name__} has been called {count} times")
        return func(*args, **kwargs)
        
    return wrapper

@call_counter
def compute(x, y):
    return x * y

print(compute(3, 4))
# 输出: 
# Function compute has been called 1 times
# 12
print(compute(5, 6))
# 输出: 
# Function compute has been called 2 times
# 30
```

先复习一下`*args`和`**kwargs`以及其参数传递机制。

`*args`是可变位置参数：

- 作用：接收任意数量的位置参数(positional arguments)
- 类型：将传入的参数打包成元组(tuple)
- 符号：单星号(`*`)
- 命名：`args`是约定俗成的名称，可以替换为其他名称（如`*params`）

`**kwargs`是可变关键字参数：

- 作用：接收任意数量的关键字参数(keyword arguments)
- 类型：将传入的参数打包成字典(dict)
- 符号：双星号(**)
- 命名：kwargs是约定俗成的名称（"keyword arguments"的缩写）

参数传递的四种情况：

调用方式 | args接收内容 | kwargs接收内容
---|---|---
func(1, 2) | (1, 2) | {}
func(a=1, b=2) | () | {'a':1, 'b':2}
func(1, b=2) | (1,) | {'b':2}
func(*[1,2], **{'c':3}) | (1, 2) | {'c':3}

下面是另外一个参数验证装饰器的例子。

```python
def validate_non_negative(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Negative values not allowed")
        for value in kwargs.values():
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("Negative values not allowed")
        return func(*args, **kwargs)
    return wrapper

@validate_non_negative
def calculate_area(width, height):
    return width * height

calculate_area(5, 3)
# 输出: 不报错
calculate_area(-2, 4)
# 输出: ValueError: Negative values not allowed
```

下面看一个函数调用日志记录的例子。

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        arg_str = ', '.join([str(a) for a in args] + [f"{k}={v}" for k,v in kwargs.items()])
        print(f"Calling {func.__name__}({arg_str})")
        return func(*args, **kwargs)
    return wrapper

@log_call
def power(base, exp=1):
    return base ** exp

power(2, 3) # args=(2,3)
# 输出: Calling power(2, 3)

power(2, exp=4) # args=(2,), kwargs={'exp',4}
# 输出: Calling power(2, exp=4)
```

`nonlocal`可以跨越多层嵌套函数查找变量。

```python
def outer():
    x = 10
    
    def middle():
        def inner():
            nonlocal x  # 找到middle外围的outer中的x
            x += 1
            return x
        return inner
    return middle

f = outer()()
print(f())  # 输出: 11
print(f())  # 输出: 12
```

`nonlocal`和`global`的区别：

- `nonlocal`用于嵌套函数，查找最近的外围作用域中的变量
- `global`直接查找模块全局作用域中的变量

```python
x = 0  # 全局变量

def test():
    x = 10  # 局部变量
    
    def inner():
        global x  # 引用全局x，不是test中的x
        x += 1
        
    inner()
    print("local x:", x)  # 输出: local x: 10
    print("global x:", globals()['x'])  # 输出: global x: 1

test()
```

虽然`nonlocal`提供了灵活性，但过度使用可能导致代码难以理解和维护。建议：

1. 对于简单状态保持，优先考虑使用闭包和`nonlocal`
2. 对于复杂状态，考虑使用类来更清晰地管理状态
3. 避免深层嵌套的`nonlocal`使用，这会增加代码阅读难度
4. 在团队协作项目中，谨慎使用`nonlocal`并添加适当注释

闭包和`nonlocal`变量访问通常比局部变量访问稍慢，因为Python需要在运行时查找外围作用域。在性能关键的代码中，可以考虑将频繁访问的非局部变量作为参数传递或使用其他设计模式。

下面我们看看一些有意思的示例。

首先，使用`@wraps(func)`可以保持函数元信息，直接使用`wrapper`会导致原函数的`__name__`、`__doc__`等元信息丢失。

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def calculate(x, y):
    """Calculate the sum of two numbers"""
    return x + y

print(calculate.__name__)
# 输出: 'wrapper'，期望是 'calculate'
print(calculate.__doc__)
# 输出: 'Wrapper docstring'，期望是原函数的文档字符串
```

分析一下原因。

每个函数对象都包含这些重要属性：

- `__name__`：函数名称（用于调试和日志）
- `__doc__`：文档字符串（help()函数和文档工具依赖）
- `__module__`：所属模块
- `__annotations__`：类型注解
- `__dict__`：其他自定义属性

装饰器语法 @decorator 本质上是：`calculate = simple_decorator(calculate)`。这导致，原函数`calculate`被替换为`wrapper`函数，所有函数属性都来自`wrapper`而非原函数`calculate`。

通过`@wraps(func)`来解决上面的问题。

```python
from functools import wraps

def simple_decorator(func):
    @wraps(func) # 修复点：保留原函数元数据
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def calculate(x, y):
    """Calculate the sum of two numbers"""
    return x + y

print(calculate.__name__)
# 输出: calculate
print(calculate.__doc__)
# 输出: Calculate the sum of two numbers
```

`@wraps(func)`实际上执行了以下操作：

```python
wrapper.__name__ = func.__name__
wrapper.__doc__ = func.__doc__
wrapper.__module__ = func.__module__
wrapper.__annotations__ = func.__annotations__
# 以及更新__dict__等属性
```

在理解了`@wraps(func)`的实现原理，我们可以在不使用`wraps`情况下，通过手动复制属性。

```python
from functools import wraps

def simple_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    # 手动复制关键属性
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__dict__.update(func.__dict__)
    return wrapper

@simple_decorator
def calculate(x, y):
    """Calculate the sum of two numbers"""
    return x + y

print(calculate.__name__)
# 输出: calculate
print(calculate.__doc__)
# 输出: Calculate the sum of two numbers
```

下面讨论一下反模式与常见错误。

错误1：错误地修改参数。

在下面的示例中，我们尝试在装饰器中修改了参数的值，导致原函数的行为发生了变化。这种做法可能会导致代码难以理解和维护，尤其是在函数参数较多时。

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        args = list(args)  # 转为可变列表

        # 如果第一个参数是列表，则对列表中的每个元素加1
        if isinstance(args[0], list): 
            for i in range(len(args[0])):
                args[0][i] += 1
        # 如果第一个参数是数字，则加1
        else:  
            args[0] += 1
        return func(*args, **kwargs)

    return wrapper


@bad_decorator
def func(a, b):
    print(a, b)


x, y = 1, 2
func(x, y)  # 输出: 2 2
print(x, y)  # 输出: 1 2

x, y = [1], [2]
func(x, y)  # 输出: 2 2
print(x, y)  # 输出: [2] [2]
```

我们看上面的代码执行过程：

调用 `func(1, 2)`等价于 `bad_decorator(func)(1, 2)`，即执行 `wrapper(1, 2)`，wrapper 内部操作如下，最终输出`func(2, 2)`打印 `2 2`。

```python
args = (1, 2)           # 原始参数元组
args = list(args)       # 转为可变列表 [1, 2]
args[0] += 1            # 修改第一个元素 → [2, 2]
return func(*[2, 2])    # 解包后等价于 func(2, 2)
```

当执行`func([1], [2])`时，调用链是`func([1], [2]) → bad_decorator(func)([1], [2]) → wrapper([1], [2])`。 `wrapper` 内部操作如下：

```python
args = ([1], [2])          # 原始参数元组
args = list(args)          # 转为可变列表 [[1], [2]]

# 处理第一个参数（列表）
for i in range(len(args[0])):  # args[0]是[1]
    args[0][i] += 1            # 修改为 [2]

# 第二个参数（[2]）未被处理
return func(*args)          # 解包后等价于 func([2], [2])
```

虽然代码执行后输出符合预期，但存在以下问题：

- 隐式修改输入参数，调用者可能不知道 `func(1, 2)` 实际会修改第一个参数，破坏透明性。
- 副作用风险，如果传入的是可变对象（如列表，x, y = [1], [2]），原始数据`x`的值会被意外修改。
- 类型破坏，强制转换 `args` 为列表可能引发问题（如传入不可迭代对象时）。上面代码额外的对第一个参数是列表还是数字进行了判断。

建议做如下修改：

- 保持输入数据不变
- 明确表达意图
- 避免隐蔽的副作用

```python
def bad_decorator(func):
    def wrapper(a, b, *args, **kwargs):
        if isinstance(a, list):
            # 明确选择：返回新列表（推荐）或修改原列表
            new_a = [x + 1 for x in a]  # 安全副本
            return func(new_a, b, *args, **kwargs)
        else:
            return func(a + 1, b, *args, **kwargs)

    return wrapper


@bad_decorator
def func(a, b):
    print(a, b)


x, y = 1, 2
func(x, y)  # 输出: 2 2
print(x, y)  # 输出: 1 2

x, y = [1], [2]
func(x, y)  # 输出: 2 2
print(x, y)  # 输出: [1] [2]
```

错误2：忽略kwargs。

```python
def unreliable_decorator(func):
    def wrapper(*args):  # 没有接收kwargs
        return func(*args)  # 丢失所有关键字参数
    return wrapper

@unreliable_decorator
def greet(name, message="Hello"):
    print(f"{message}, {name}!")

greet("Alice")                # 正常输出: Hello, Alice!
greet("Bob", message="Hi")    # 报错: TypeError: wrapper() got an unexpected keyword argument 'message'
```
