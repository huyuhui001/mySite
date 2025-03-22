# 高效Python90条之第12条　不要在切片里同时指定起止下标与步进

Python对切片的步进表达形式是`somelist[start:end:stride]`。

```python
x = ["red", "orange", "yellow", "green", "blue", "purple"]
odds = x[::2]
evens = x[1::2]
print(odds)  # 输出：['red', 'yellow', 'blue']
print(evens)  # 输出：['orange', 'green', 'purple']
```

下面是对bytes和Unicode类型的字符串做切片，将字符串反转。

```python
x = b'mongoose'
y = x[::-1]
print(y)  # 输出：b'esoognom'

x = '寿司'
y = x[::-1]
print(y)  # 输出：'司寿'
```

但如果把这种字符串编码成UTF-8标准的字节数据，就不能直接通过`x[::-1]`方法来反转了，而是需要通过解码来实现。

```python
w = "寿司"

# 无法直接反转
x = w.encode("utf-8")
y = x[::-1]
print(y)  # 输出：b'\xb8\x8f\xe5\xbf\xaf\xe5'
z = y.decode("utf-8") # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb8 in position 0: invalid start byte

# 解码后再反转
x = w.encode("utf-8")
y = x.decode("utf-8")[::-1]
print(y)  # 输出：'司寿'
```

看下面一些负数做步进值的例子。步进值是负数的时候，会从起始下标开始，倒着选取，一直选到终止下标所在的位置，但不包含该位置本身。

```python
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# 从第一个元素开始，每隔一个元素选取一个元素。 
print(x[::2]) # 输出：['a', 'c', 'e', 'g']
# 从最后一个元素开始，每隔一个元素选取一个元素。
print(x[::-2]) # 输出：['h', 'f', 'd', 'b']   
# 从第三个元素开始，每隔一个元素选取一个元素。
print(x[2::2]) # 输出：['c', 'e', 'g']
# 从倒数第二个元素开始，每隔一个元素选取一个元素。
print(x[-2::-2]) # 输出：['g', 'e', 'c', 'a']
# 从倒数第二个元素开始，每隔一个元素选取一个元素，直到第三个元素。
print(x[-2:2:-2]) # 输出：['g', 'e']
# 从第三个元素开始，每隔一个元素选取一个元素，直到第三个元素。
print(x[2:2:-2]) # 输出：[]
```

各种起止位和正负步进值会让代码可读性下降，实践中的建议是，不要把起止下标和步进值同时写在切片里。如果必须指定步进，那么尽量采用正数，而且要把起止下标都留空。即便必须同时使用步进值与起止下标，也应该考虑分成两次来写。

下面是建议做法。

示例 1：避免同时指定起止下标和步进值

```python
a = ["a", "b", "c", "d", "e", "f", "g", "h"]

# 不推荐写法：同时指定起止下标和步进值
subset = a[1:7:2]  # 从索引 1 到索引 7，每隔 2 个元素选取一个
print("Subset:", subset)  # 输出：Subset: ['b', 'd', 'f']

# 推荐写法：
# 先切片
subset = a[1:7]
# 再步进，直接省略起止下标，只用步进值
subset = subset[::2]
print("Subset:", subset)  # 输出：Subset: ['b', 'd', 'f']
```

示例 2：使用 itertools.islice

```python
import itertools

a = ["a", "b", "c", "d", "e", "f", "g", "h"]

# 使用 itertools.islice，可以同时指定起始位置、终止位置和步进值，而不会影响代码的可读性。
subset = list(itertools.islice(a, 1, 7, 2))
print("Subset using itertools.islice:", subset)  # 输出：Subset using itertools.islice: ['b', 'd', 'f']
```

要点

- 同时指定切片的起止下标与步进值理解起来会很困难。
- 如果要指定步进值，那就省略起止下标，而且最好采用正数作为步进值，尽量别用负数。
- 不要把起始位置、终止位置与步进值全都写在同一个切片操作里。如果必须同时使用这三项指标，那就分两次来做（其中一次隔位选取，另一次做切割）​，也可以改用`itertools`内置模块里的`islice`方法。
