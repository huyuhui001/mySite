# 高效Python90条之第15条　不要过分依赖给字典添加条目时所用的顺序

要点

- 从Python 3.7版开始，我们就可以确信迭代标准的字典时所看到的顺序跟这些键值对插入字典时的顺序一致。
- 在Python代码中，我们很容易就能定义跟标准的字典很像但本身并不是dict实例的对象。对于这种类型的对象，不能假设迭代时看到的顺序必定与插入时的顺序相同。
- 如果不想把这种跟标准字典很相似的类型也当成标准字典来处理，那么可以考虑这样三种办法。第一，不要依赖插入时的顺序编写代码；第二，在程序运行时明确判断它是不是标准的字典；第三，给代码添加类型注解并做静态分析。

在Python之前的版本中，迭代字典（dict）时所看到的顺序是随机的，不一定与当初把这些键值对添加到字典时的顺序相同。也就是说，字典不保证迭代顺序与插入顺序一致。是因为字典类型以前是用哈希表算法来实现的（这个算法通过内置的hash函数与一个随机的种子数来运行，而该种子数会在每次启动Python解释器时确定）​。所以，这样的机制导致这些键值对在字典中的存放顺序不一定会与添加时的顺序相同，而且每次运行程序的时候，存放顺序可能都不一样。

从Python 3.6开始，字典会保留这些键值对在添加时所用的顺序，而且Python 3.7版的语言规范正式确立了这条规则。于是，在新的Python里，总是能够按照当初创建字典时的那套顺序来遍历这些键值对。

示例 1：标准字典的迭代顺序

```python
my_dict = {"a": 1, "b": 2, "c": 3}

for key in my_dict:
    print(key, my_dict[key])
# 输出：
# a 1
# b 2
# c 3
```

对于那些类似字典但并非标准 `dict` 实例的对象。这些对象可能不保证迭代顺序与插入顺序一致。

示例 2：自定义字典类

看下面的代码，定义一个标准的字典`votes`，通过函数`populate_ranks`来对字典`votes`按照值的大小进行倒序排列，保存到字典`ranks`中。再通过函数`get_winner`从字典`ranks`中读取第一个值（排名第一）。

```python
# 设定一个字典，包含动物的名字和对应的票数。
votes = {"otter": 1281, "polar bear": 587, "fox": 863}

# 定义一个函数，把票数排序并把名次关联到名字上。
def populate_ranks(votes, ranks):
    # 获取键的列表，即所有动物的名称
    names = list(votes.keys())
    # 按照票数对名字进行倒序排列
    # votes.get是一个方法，它接受一个键并返回该键对应的值，比如接受键otter，返回其对应值1281
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1): # 遍历排序后的动物名称，并生成排名
        ranks[name] = i # 将每个动物的排名存储在ranks字典中

# 获取人气最高的动物
def get_winner(rank):
    # iter(rank)是返回rank字典的迭代器，迭代器会按字典的键的顺序返回键。
    # next(iter(rank))会获取迭代器的第一个元素，即字典的第一个键。
    return next(iter(rank))

rank = {}
populate_ranks(votes, rank)
print(rank)
# 输出：
# {'otter': 1, 'fox': 2, 'polar bear': 3}
winner = get_winner(rank)
print(winner)
# 输出：
# otter
```

下面我们定义一个类`SortedDict`，继承自`MutableMapping`，实现了一个有序字典。我们定义了`__iter__`，进行升序迭代。

```python
from collections.abc import MutableMapping

votes = {"otter": 1281, "polar bear": 587, "fox": 863}

def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

def get_winner(rank):
    return next(iter(rank))

# 定义一个类，继承自 MutableMapping，实现了一个有序字典。
class SortedDict(MutableMapping):
    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
    
    # 返回一个迭代器，按字典键的升序迭代。
    def __iter__(self):
        keys = list(self._data.keys()) # 获取所有键
        keys.sort() # 对键进行升序排序，即按名字排序
        for key in keys: # 按排序后的键顺序迭代
            yield key

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)


sorted_rank = SortedDict()
populate_ranks(votes, sorted_rank)
print(sorted_rank)
# 输出：
# {'otter': 1, 'fox': 2, 'polar bear': 3}
winner = get_winner(sorted_rank)
print(winner)
# 输出：
# fox
```

上面`print(winner)`没有输出`otter`，而是输出`fox`，显然不正确，这是因为`get_winner`函数总是假设，迭代字典时的顺序应该跟`populate_ranks`函数当初向字典中插入数据时的顺序一样。原因如下：

`print(sorted_rank)` 调用了 `SortedDict` 的 `__repr__` 方法，该方法返回 `self.data` 的字符串表示形式。`self.data` 是一个普通字典，其迭代顺序就是插入顺序。`populate_ranks` 函数在填充 `sorted_rank` 时，按票数降序插入键值对，因此 `otter` 是第一个插入的键，所以 `print(sorted_rank)` 输出 `otter` 排第一个

`get_winner` 函数通过 `next(iter(rank))` 获取字典的第一个键。`SortedDict` 的 `__iter__` 方法按字母顺序返回键，因此 `fox` 是按字母顺序的第一个键，所以 `get_winner` 返回 `fox`。

修改方法1，重新实现`get_winner`函数，使它不再假设`ranks`字典总是能按照固定的顺序来迭代。这是最保险、最稳妥的一种方案。

```python
def get_winner(rank):
    for name, rank in rank.items():
        if rank == 1:
            return name
```

修改方法2，在函数开头先判断`ranks`是不是预期的那种标准字典（`dict`）​。如果不是，就抛出异常。

```python
def get_winner(rank):
    if not isinstance(rank, dict):
        raise TypeError("must provide a dict instance")
    return next(iter(rank))
```

修改方法3，通过类型注解（type annotation）来保证传给`get_winner`函数的确实是个真正的`dict`实例，而不是那种行为跟标准字典类似的`MutableMapping`。下面是修改后的完整代码，保存在文件`_tmp.py`。

```python
from collections.abc import MutableMapping
from typing import Dict

# 设定一个字典，包含动物的名字和对应的票数。
votes = {"otter": 1281, "polar bear": 587, "fox": 863}


# 定义一个函数，把票数排序并把名次关联到名字上。
def populate_ranks(votes: Dict[str, int], ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


# 获取人气最高的动物
def get_winner(rank: Dict[str, int]) -> str:
    return next(iter(rank))


# 定义一个类，继承自 MutableMapping，实现了一个有序字典。
class SortedDict(MutableMapping[str, int]):
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]
    
    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())  # 获取所有键
        keys.sort(key=lambda k: self.data[k], reverse=False)  # 按票数降序排序
        for key in keys:  # 按排序后的键顺序迭代
            yield key

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)


sorted_rank = SortedDict()
populate_ranks(votes, sorted_rank)
print(sorted_rank)
winner = get_winner(sorted_rank)
print(winner)
```

执行下面的命令对_tmp.py进行静态检查，可以看到错误。

```bash
python3 -m mypy --strict _tmp.py
```

错误信息：

```bash
_tmp.py:11: error: Argument "key" to "sort" of "list" has incompatible type overloaded function; expected "Callable[[str], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"  [arg-type]
_tmp.py:23: error: Function is missing a return type annotation  [no-untyped-def]
_tmp.py:23: note: Use "-> None" if function does not return a value
_tmp.py:26: error: Function is missing a type annotation  [no-untyped-def]
_tmp.py:29: error: Function is missing a type annotation  [no-untyped-def]
_tmp.py:32: error: Function is missing a type annotation  [no-untyped-def]
_tmp.py:35: error: Function is missing a type annotation  [no-untyped-def]
_tmp.py:41: error: Function is missing a type annotation  [no-untyped-def]
_tmp.py:44: error: Function is missing a type annotation  [no-untyped-def]
_tmp.py:48: error: Call to untyped function "SortedDict" in typed context  [no-untyped-call]
_tmp.py:49: error: Argument 2 to "populate_ranks" has incompatible type "SortedDict"; expected "dict[str, int]"  [arg-type]
_tmp.py:51: error: Argument 1 to "get_winner" has incompatible type "SortedDict"; expected "dict[str, int]"  [arg-type]
```

最后2行的错误信息表示 `populate_ranks` 和 `get_winner` 函数的参数类型与实际传入的类型不匹配。`populate_ranks` 函数期望第二个参数是一个普通的字典（`dict[str, int]`），而 `SortedDict` 是一个自定义的类，虽然它继承自 `MutableMapping`，但并不是一个普通的字典。

下面是修改后的代码。

```python
from collections.abc import MutableMapping
from typing import Dict

# 设定一个字典，包含动物的名字和对应的票数。
votes = {"otter": 1281, "polar bear": 587, "fox": 863}


# 定义一个函数，把票数排序并把名次关联到名字上。
def populate_ranks(votes: Dict[str, int], ranks: MutableMapping[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


# 获取人气最高的动物
def get_winner(rank: MutableMapping[str, int]) -> str:
    return next(iter(rank))


# 定义一个类，继承自 MutableMapping，实现了一个有序字典。
class SortedDict(MutableMapping[str, int]):
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]
    
    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())  # 获取所有键
        keys.sort(key=lambda k: self.data[k], reverse=False)  # 按票数降序排序
        for key in keys:  # 按排序后的键顺序迭代
            yield key

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)


sorted_rank = SortedDict()
populate_ranks(votes, sorted_rank)
print(sorted_rank)
# 输出：
# {'otter': 1, 'fox': 2, 'polar bear': 3}
winner = get_winner(sorted_rank)
print(winner)
# 输出：
# otter
```

总结一下，为了避免依赖字典的插入顺序，可以采取以下三种策略：

1.不依赖插入顺序编写代码。尽量编写不依赖插入顺序的代码。这样可以确保代码在面对不同类型的字典对象时仍然能够正确运行。

示例 3：不依赖插入顺序

```python
my_dict = {"a": 1, "b": 2, "c": 3}
for key in sorted(my_dict):
    print(key, my_dict[key])
# 输出：
# a 1
# b 2
# c 3
```

2.在程序运行时明确判断是否为标准字典。在程序运行时，可以通过 `isinstance` 函数明确判断对象是否为标准字典。

示例 4：运行时判断是否为标准字典

```python
class CustomDict:
    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

def ProcessDict(d):
    if not isinstance(d, dict):
        raise TypeError("Expected a standard dict instance")
    for key in d:
        print(key, d[key])

custom_dict = CustomDict()
custom_dict["a"] = 1
custom_dict["b"] = 2
custom_dict["c"] = 3

try:
    ProcessDict(custom_dict)
except TypeError as e:
    print(e)

# 输出：
# Expected a standard dict instance
```

3.给代码添加类型注解并做静态分析。通过给代码添加类型注解，并使用静态分析工具（如 `mypy`），可以确保传入的对象是标准字典。

示例 5：添加类型注解

```python
from typing import Dict

def process_dict(d: Dict[str, int]):
    for key in d:
        print(key, d[key])

my_dict: Dict[str, int] = {"a": 1, "b": 2, "c": 3}
process_dict(my_dict)
# 输出：
# a 1
# b 2
# c 3
```
