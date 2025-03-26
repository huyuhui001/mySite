# 高效Python90条之第16条　用get处理键不在字典中的情况，不要使用in与KeyError

要点

- 有四种办法可以处理键不在字典中的情况：`in`表达式、`KeyError`异常、`get`方法与`setdefault`方法。
- 如果跟键相关联的值是像计数器这样的基本类型，那么`get`方法就是最好的方案；如果是那种构造起来开销比较大，或是容易出异常的类型，那么可以把这个方法与赋值表达式结合起来使用。
- 即使看上去最应该使用`setdefault`方案，也不一定要真的使用`setdefault`方案，而是可以考虑用`defaultdict`取代普通的`dict`。

字典有三种基本的交互操作：访问、赋值以及删除键值对。

在Python中处理字典中键不存在的几种主要的方法：

- `in` 表达式；`in` 表达式可以用来检查字典中是否存在某个键。如果键存在，则直接访问该键的值；如果键不存在，则可以设置一个默认值。
- `KeyError` 异常；通过捕获 `KeyError` 异常来处理键不存在的情况。这种方法在键不存在时会抛出一个异常，然后可以捕获这个异常并设置一个默认值。
- `get` 方法和；`get` 方法是处理键不存在的最简洁方式。它允许你指定一个默认值，如果键不存在，则返回该默认值。
- `setdefault` 方法；`setdefault` 方法会在键不存在时设置一个默认值，并返回该默认值。如果键已经存在，则返回该键的值。
- `defaultdict` 方法； 适用于需要频繁处理键不存在的情况，特别是默认值的构造开销较大或容易出异常时。

示例代码。

```python
my_dict = {"a": 9, "b": 2}

### 1.使用in表达式
if "c" in my_dict:
    value = my_dict["c"]
else:
    value = 0  # 默认值

my_dict["c"] = value
print(my_dict)
# 输出：{'a': 9, 'b': 2, 'c': 9}


### 2.使用KeyError异常
try:
    value = my_dict["c"]
except KeyError:
    value = 0  # 默认值

my_dict["c"] = value
print(my_dict)
# 输出：{'a': 9, 'b': 2, 'c': 0}


### 3.使用get方法获取值，如果键不存在则返回默认值
value = my_dict.get("c", 0)

my_dict["c"] = value
print(my_dict)
# 输出：{'a': 9, 'b': 2, 'c': 0}


### 4.使用setdefault方法获取值，如果键不存在则设置默认值
value = my_dict.setdefault("c", 0)
print(my_dict)
# 输出：{'a': 9, 'b': 2, 'c': 0}
```

如果需要频繁处理键不存在的情况，特别是当默认值的构造开销较大或容易出异常时，可以考虑使用 `defaultdict`。

`defaultdict` 是 `collections` 模块中的一个内置类，它继承自普通的 `dict`，但提供了一个默认值的工厂函数。
当我们访问一个不存在的键时，`defaultdict` 会自动调用这个工厂函数来生成默认值，并将这个默认值添加到字典中。

`defaultdict` 的构造函数接受一个可调用对象作为参数。这个可调用对象会在访问不存在的键时被调用来生成默认值。
在下面的示例代码`defaultdict(int)`中，`int` 是一个可调用对象，调用 `int()` 会返回 `0`。

```python
from collections import defaultdict

# 使用 defaultdict 指定默认值的工厂函数
my_dict = defaultdict(int)  # 默认值为 0

# 初始化字典
my_dict["a"] = 1
my_dict["b"] = 2

# 访问不存在的键时会自动调用工厂函数生成默认值
value = my_dict["c"]

print(my_dict)
# 输出：defaultdict(<class 'int'>, {'a': 1, 'b': 2, 'c': 0})
```

如果字典`my_dict`里面保存的数据比较复杂，例如列表（list）​，操作类似。示例如下。

```python
my_dict = {
    "华北": ["北京", "天津"],
    "华东": ["上海", "南京"],
    "华南": ["广州", "深圳"],
}

key = "华中"
city = "武汉"

### 1.使用in表达式
if key in my_dict:
    value = my_dict[key]
else:
    my_dict[key] = value = []  # 默认值

value.append(city)
print(my_dict)
# 输出：{'华北': ['北京', '天津'], '华东': ['上海', '南京'], '华南': ['广州', '深圳'], '华中': ['武汉']}


### 2.使用KeyError异常
try:
    value = my_dict[key]
except KeyError:
    my_dict[key] = value = []  # 默认值

value.append(city)
print(my_dict)
# 输出：{'华北': ['北京', '天津'], '华东': ['上海', '南京'], '华南': ['广州', '深圳'], '华中': ['武汉']}


### 3.使用get方法获取值，如果键不存在则返回默认值
value = my_dict.get(key)
if value is None:
    my_dict[key] = value = []  # 默认值

value.append(city)
print(my_dict)
# 输出：{'华北': ['北京', '天津'], '华东': ['上海', '南京'], '华南': ['广州', '深圳'], '华中': ['武汉']}


### 4.使用setdefault方法获取值，如果键不存在则设置默认值
value = my_dict.setdefault(key, [])
print(my_dict)
# 输出：{'华北': ['北京', '天津'], '华东': ['上海', '南京'], '华南': ['广州', '深圳'], '华中': []}
value.append(city)
print(my_dict)
# 输出：{'华北': ['北京', '天津'], '华东': ['上海', '南京'], '华南': ['广州', '深圳'], '华中': ['武汉']}
```

上面代码中第三种使用`get`的情形，如果写成下面这样是不对的，因为`my_dict.get("key", [])` 返回了一个临时的列表 `[]`，但这个列表并没有被存储在字典`my_dict`中。

```python
value = my_dict.get(key, [])
value.append(city)
print(my_dict)
```

上面代码中第四种使用`setdefault`的情形，有个点需要注意：在字典里面没有这个键时，`setdefault`方法会把默认值直接放到字典里，对比2个`print`语句可以看到这个情况。这就相当于每次调用时，不管字典里有没有这个键，都得分配一个列表实例，这有可能产生比较大的性能开销。

只有在少数几种情况下用`setdefault`处理缺失的键才是最简短的方式，例如这种情况：与键相关联的默认值构造起来开销很低且可以变化，而且不用担心异常问题（例如list实例）​。在这种特殊的场合，或许可以用`setdefault`方法取代行数稍微多一些的`get`方案。即便如此，一般也应该优先考虑用`defaultdict`（带默认值的字典）取代`dict`​。

对于`defaultdict`的代码可以做如下改写。

这里需要注意一点，`my_dict[key].append(city)` 这句代码在访问键 `key` 时，如果键不存在，`defaultdict` 会自动调用工厂函数 `list()` 生成一个默认值 `[]`，并将这个默认值存储在字典中。然后，它会在生成的默认值上执行 `append` 操作。最后2个print语句体现了这2个动作（插入默认值、`append` 操作）。

```python
from collections import defaultdict

# 使用 defaultdict 指定默认值的工厂函数
my_dict = defaultdict(list)  # 默认值为 []

# 初始化字典
initial_data = {
    "华北": ["北京", "天津"],
    "华东": ["上海", "南京"],
    "华南": ["广州", "深圳"],
}

# 将普通字典的内容初始化到 defaultdict 中
for key, value in initial_data.items():
    my_dict[key] = value

key = "华中"
city = "武汉"

# 直接访问不存在的键，defaultdict 会自动调用工厂函数生成默认值
my_dict[key]
print(my_dict)
# 输出：defaultdict(<class 'list'>, {'华北': ['北京', '天津'], '华东': ['上海', '南京'], '华南': ['广州', '深圳'], '华中': []})
my_dict[key].append(city)
print(my_dict)
# 输出：defaultdict(<class 'list'>, {'华北': ['北京', '天津'], '华东': ['上海', '南京'], '华南': ['广州', '深圳'], '华中': ['武汉']})
```
