# 高效Python90条之第17条　用defaultdict处理内部状态中缺失的元素，而不要用setdefault

要点

- 如果你管理的字典可能需要添加任意的键，那么应该考虑能否用内置的collections模块中的defaultdict实例来解决问题。
- 如果这种键名比较随意的字典是别人传给你的，你无法把它创建成defaultdict，那么应该考虑通过get方法访问其中的键值。然而，在个别情况下，也可以考虑改用setdefault方法，因为那样写更短。

在[第16条](./Rule16.md)中，介绍了如果字典不是自己创建的，那么对其中缺失的键可以考虑用四种办法解决。在这四种办法中，`get`方案要胜过利用`in`表达式和`KeyError`异常这两种方案，在某些情况下，`setdefault`应该是代码最简短的办法。

处理字典中缺失的键是一个常见的问题。虽然 `setdefault` 方法可以解决这个问题，但 `defaultdict` 提供了一种更高效的方式来处理这种情况。

`defaultdict` 是 `collections` 模块中的一个类，它继承自普通的 `dict`，且提供了一个默认值的工厂函数。当你访问一个不存在的键时，`defaultdict` 会自动调用这个工厂函数来生成默认值，并将这个默认值存储在字典中。

`defaultdict` 在处理缺失键时的性能通常优于 `setdefault`，因为它避免了显式地检查键是否存在和赋值操作。

下面示例代码通过 `defaultdict` 生成了一个字典 `visits` 。

```python
from collections import defaultdict

# 使用 defaultdict 指定默认值的工厂函数
visits = defaultdict(list)  # 默认值为 []

# 初始化字典
initial_data = {
    "华北": {"北京", "天津"},
    "华东": {"上海", "南京"},
    "华南": {"广州", "深圳"},
}

# 将普通字典的内容初始化到 defaultdict 中
for key, value in initial_data.items():
    visits[key] = value

print(visits)
# 输出：defaultdict(<class 'list'>, {'华北': {'天津', '北京'}, '华东': {'上海', '南京'}, '华南': {'深圳', '广州'}})
```

无论字典 `visits` 中有没有这个城市名称（比如下例中的 `长沙` ），都可以通过 `setdefault` 方法把新的城市添加到对应的集合里，这要比利用 `get` 方法与赋值表达式实现的方案短很多。

从代码的简洁性，对比下面两种方案：

```python
# 使用setdefault方法
visits.setdefault("华中", set()).add("武汉")
print(visits)
# 输出：defaultdict(<class 'list'>, {'华北': {'北京', '天津'}, '华东': {'上海', '南京'}, '华南': {'深圳', '广州'}, '华中': {'武汉'}})

# 使用get方法
if (city := visits.get("华中")) is None:
    visits["华中"] = city = set()
city.add("长沙")
print(visits)
# 输出：defaultdict(<class 'list'>, {'华北': {'天津', '北京'}, '华东': {'上海', '南京'}, '华南': {'深圳', '广州'}, '华中': {'长沙'}})
```

实际应用中，比如我们经常需要用字典实例来维护某类对象的内部状态，这种情况下，这个字典需要我们自己明确地创建。

基于上例，我们写一个类，把上面的逻辑封装到方法中，使其他用户可以调用该方法来访问字典中保存的动态的内部状态。

```python


```


















## 2. `setdefault` 的适用场景

### 2.1 处理外部传入的字典
如果你处理的是外部传入的字典，而你无法控制其类型，那么 `setdefault` 是一个合适的选择。`setdefault` 可以在普通字典上直接使用，而不需要将其转换为 `defaultdict`。

#### 示例代码
```python
# 外部传入的普通字典
my_dict = {}

# 使用 setdefault 处理缺失的键
my_dict.setdefault("key", []).append("value")

print(my_dict)  # 输出：{'key': ['value']}
```

### 2.2 代码更短
在某些情况下，`setdefault` 的代码更短，尤其是在需要显式设置默认值时。

#### 示例代码
```python
# 使用 setdefault
my_dict = {}
my_dict.setdefault("key", []).append("value")

# 使用 defaultdict
my_dict = defaultdict(list)
my_dict["key"].append("value")
```

## 3. 实际应用示例

### 3.1 管理内部状态
假设你正在管理一个内部状态，需要动态地添加键值对。使用 `defaultdict` 可以简化代码并提高性能。

#### 示例代码
```python
from collections import defaultdict

# 使用 defaultdict 管理内部状态
state = defaultdict(list)

# 动态添加键值对
state["user1"].append("login")
state["user2"].append("logout")

print(state)  # 输出：defaultdict(<class 'list'>, {'user1': ['login'], 'user2': ['logout']})
```

### 3.2 处理外部传入的字典
如果你处理的是外部传入的字典，而你无法控制其类型，那么 `setdefault` 是一个合适的选择。

示例代码

```python
# 外部传入的普通字典
external_dict = {}

# 使用 setdefault 处理缺失的键
external_dict.setdefault("key", []).append("value")

print(external_dict)  # 输出：{'key': ['value']}
```


- **`defaultdict`**：适用于管理内部状态，自动处理缺失的键，代码更简洁，性能更优。
- **`setdefault`**：适用于处理外部传入的字典，代码更短，尤其是在需要显式设置默认值时。














