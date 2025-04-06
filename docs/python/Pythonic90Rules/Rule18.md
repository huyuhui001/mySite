# 高效Python90条之第18条　利用`__missing__`构造依赖键的默认值

要点

- 如果创建默认值需要较大的开销，或者可能抛出异常，那就不适合用`dict`类型的`setdefault`方法实现。
- 传给`defaultdict`的函数必须是不需要参数的函数，所以无法创建出需要依赖键名的默认值。
- 如果要构造的默认值必须根据键名来确定，那么可以定义自己的`dict`子类并实现`__missing__`方法。

我们可以利用内置的`dict`类型提供了`setdefault`方法来处理缺失的键，大多数情况下可以通过内置的`collections`模块中的`defaultdict`来处理缺失的键。实际中也有一些任务是`setdefault`和`defaultdict`可能都处理不好，这种情况下，可以尝试通过定义自己的 `dict` 子类并实现 `__missing__` 方法来解决问题。

我们先看 `setdefault` 和 `defaultdict` 的局限性。

`setdefault` 方法可以为缺失的键设置默认值，但是（1）它需要显式调用，（2）并且默认值的构造函数不能接受键名作为参数。比如，下面例子中，`setdefault` 方法的默认值是一个空列表 `[]`。这个默认值是通过 `list()` 构造函数生成的，而 `list()` 构造函数不接受任何参数。

```python
my_dict = {}
my_dict.setdefault("key", []).append("value")
print(my_dict)  # 输出：{'key': ['value']}
```

`defaultdict` 可以自动处理缺失的键，但它要求默认值的构造函数是无参数的。在下面的例子中，`defaultdict` 的默认值构造函数是 `list()`，它也不接受任何参数。

```python
from collections import defaultdict

my_dict = defaultdict(list)
my_dict["key"].append("value")
print(my_dict)  # 输出：defaultdict(<class 'list'>, {'key': ['value']})
```

再举例 `defaultdict` 的限制的例子。假设我们希望默认值是一个字典，其中包含键名作为某个字段的值。`defaultdict` 无法直接实现这一点，因为它的默认值构造函数不能接受键名作为参数。

```python
from collections import defaultdict

# 假设我们希望默认值是一个字典，其中包含键名
def default_value():
    return {"name": "default"}

my_dict = defaultdict(default_value)
print(my_dict["key1"])  # 输出：{'name': 'default'}
```

为了构造依赖键名的默认值，可以定义自己的 `dict` 子类并实现 `__missing__` 方法。`__missing__` 方法会在访问缺失的键时被调用，并返回默认值。

```python
class MyDict(dict):
    def __missing__(self, key):
        # 构造默认值，可以依赖键名
        self[key] = value = f"Default_{key}"
        return value

# 创建一个 MyDict 实例
my_dict = MyDict()

# 访问一个不存在的键
print(my_dict["key1"])  # 输出：Default_key1
print(my_dict)  # 输出：{'key1': 'Default_key1'}

# 再次访问同一个键
print(my_dict["key1"])  # 输出：Default_key1
```

看下面例子，假设我们需要根据键名动态生成默认值，例如生成一个默认的用户配置，当键名不符合预设规则时需要抛出异常或进行其它处理。比如下例中，键名 `invalid-key` 包含连字符 `-`，这不符合 [Python标识符的规则](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)。

```python
class UserConfigDict(dict):
    def __missing__(self, key):
        # 验证用户名称是否合法
        if not key.isidentifier():
            raise KeyError(f"Invalid user name: {key}")

        # 根据键名生成默认值
        default_config = {
            "name": key,
            "settings": {"theme": "light", "notifications": True, "language": "en"},
        }

        # 将默认配置存储到字典中
        self[key] = default_config
        return default_config

    def get_user_config(self, user_name):
        # 获取用户的配置，如果用户不存在，则生成默认配置
        return self[user_name]

    def update_user_config(self, user_name, config_updates):
        # 更新用户的配置
        if user_name not in self:
            raise KeyError(f"User '{user_name}' does not exist.")

        self[user_name].update(config_updates)


if __name__ == "__main__":
    # 创建一个 UserConfigDict 实例
    user_configs = UserConfigDict()

    # 获取一个不存在的用户的配置，会自动生成默认配置
    Jason_config = user_configs.get_user_config("Jason")
    print(Jason_config)
    # 输出：{'name': 'Jason', 'settings': {'theme': 'light', 'notifications': True, 'language': 'en'}}
    print(user_configs)
    # 输出：{'Jason': {'name': 'Jason', 'settings': {'theme': 'light', 'notifications': True, 'language': 'en'}}}

    # 再次获取同一个用户的配置
    Jason_config = user_configs.get_user_config("Jason")
    print(Jason_config)
    # 输出：{'name': 'Jason', 'settings': {'theme': 'light', 'notifications': True, 'language': 'en'}}

    # 尝试获取一个无效的用户名称
    try:
        invalid_user_config = user_configs.get_user_config("Tom-and-Jerry")
    except KeyError as e:
        print(e)
    # 输出：Invalid user name: Tom-and-Jerry")

    # 更新用户的配置
    user_configs.update_user_config(
        "Jason", {"settings": {"theme": "dark", "language": "fr"}}
    )
    print(
        user_configs["Jason"]
    )  # 输出：{'name': 'Jason', 'settings': {'theme': 'dark', 'notifications': True, 'language': 'fr'}}
```
