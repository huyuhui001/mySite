# 高效Python90条之第20条　遇到意外状况时应该抛出异常，不要返回None

要点

- 用返回值None表示特殊情况是很容易出错的，因为这样的值在条件表达式里面，没办法与0和空白字符串之类的值区分，这些值都相当于False。
- 用异常表示特殊的情况，而不要返回None。让调用这个函数的程序根据文档里写的异常情况做出处理。
- 通过类型注解可以明确禁止函数返回None，即便在特殊情况下，它也不能返回这个值。

在 Python 中，使用 `None` 来表示特殊情况是一种常见的做法，但这种方法容易导致错误，因为 `None` 在条件表达式中被视为 `False`，这可能会与其他假值（如 `0`、`""` 等）混淆。为了避免这些问题，建议在遇到意外状况时抛出异常，而不是返回 `None`。此外，通过类型注解可以明确禁止函数返回 `None`，从而提高代码的可读性和类型安全性。

示例 1：返回 `None` 的问题。

假设一个函数 `careful_divide`，除数为 `0` 时返回 `None`。

```python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


if __name__ == "__main__":
    for i, j in [(0, 2), (10, 0)]:
        result = careful_divide(i, j)
        print(f"Result: {result}")

# 输出：
# Result: 0.0
# Result: None
```

我们也可以自定义除数为 `0` 时的处理方式，比如 `result is None`。

```python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


if __name__ == "__main__":
    for i, j in [(0, 10), (10, 0)]:
        result = careful_divide(i, j)
        if result is None:
            print("Division by zero occurred.")
        else:
            print(f"Result: {result}")
# 输出：
# Result: 0.0
# Division by zero occurred.
```

但是当我们把 `result is None` 写成 `not result`，就会发现问题，处理逻辑并没有按我们的预想执行。

```python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


if __name__ == "__main__":
    for i, j in [(0, 10), (10, 0)]:
        result = careful_divide(i, j)
        if not result:
            print("Division by zero occurred.")
        else:
            print(f"Result: {result}")
# 输出：
# Division by zero occurred.
# Division by zero occurred.
```

保留 `not result` 这种常用写法，我们进行如下代码改动，利用二元组把计算结果分成两部分返回​。元组的首个元素表示操作是否成功，第二个元素表示计算的实际值。这样写，会促使函数调用方去拆分返回值，比如 `success, result = careful_divide(i, j)`，调用方可以先看看这次运算是否成功，比如检查 `success`，然后再决定怎么处理运算结果。

```python
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


if __name__ == "__main__":
    for i, j in [(0, 10), (10, 0)]:
        success, result = careful_divide(i, j)
        if not success:
            print("Division by zero occurred.")
        else:
            print(f"Result: {result}")
# 输出：
# Result: 0.0
# Division by zero occurred.
```

但是，有些函数调用方会有可能忽略返回元组的第一个部分，例如 `_, result = careful_divide(i, j)`，最合适的做法，就是向调用方抛出异常，让调用方自己决定怎么处理​。

```python
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        raise ValueError("Division by zero occurred.") # 向调用方抛出异常


if __name__ == "__main__":
    for i, j in [(0, 10), (10, 0)]:
        # 让调用方自己决定如何处理异常
        try:
            _, result = careful_divide(i, j)
        except ValueError as e:
            print(e)
        else:
            print(f"Result: {result}")
# 输出：
# Result: 0.0
# Division by zero occurred.
```

更进一步，我们在给调用方抛出异常的基础上，通过类型注解来明确禁止函数返回 `None`。这样写，输入、输出与异常都显得很清晰，调用方出错的概率就变得很小了。

```python
def careful_divide(a: float, b:float) -> float:
    try:
        return True, a / b
    except ZeroDivisionError:
        raise ValueError("Division by zero occurred.")


if __name__ == "__main__":
    for i, j in [(0, 10), (10, 0)]:
        try:
            _, result = careful_divide(i, j)
        except ValueError as e:
            print(e)
        else:
            print(f"Result: {result}")
# 输出：
# Result: 0.0
# Division by zero occurred.
```
