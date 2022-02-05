# 第5条　用辅助函数取代复杂的表达式

Python的语法相当简明，所以有时只用一条表达式就能实现许多逻辑。

例如，要把URL之中的查询字符串拆分成键值对，那么只需要使用parse_qs函数就可以了。

```
>>> from urllib.parse import parse_qs
>>> my_value = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
>>> my_value
{'red': ['5'], 'blue': ['0'], 'green': ['']}
```

在解析查询字符串时，可以发现，有的参数可能带有多个值，有的参数可能只有一个值，还有的参数可能是空白值，另外也会遇到根本没提供这个参数的情况。

下面这三行代码分别通过get方法查询结果字典里面的三个参数，这刚好对应三种不同的情况：

```
>>> red = my_value.get('red')
>>> green = my_value.get('green')
>>> opacity = my_value.get('Opacity')
>>> print('Red        ', red)
Red         ['5']
>>> print('Green      ', green)
Green       ['']
>>> print('Opacity    ', opacity)
Opacity     None
```

通过Boolean表达式来实现把上述参数缺失与参数为空这两种情况默认值都设成0。Boolean表达式会把空白字符串、空白list以及0值，全都当成False看待。

```
>>> red = my_value.get('red', [''])[0] or 0
>>> green = my_value.get('green', [''])[0] or 0
>>> opacity = my_value.get('Opacity', [''])[0] or 0
>>> print(f'Red       : {red!r}')
Red       : '5'
>>> print(f'Green     : {green!r}')
Green     : 0
>>> print(f'Opacity   : {opacity!r}')
Opacity   : 0
```

上述代码解析：

* 因为red键存在于my_value字典（dict）里面，它对应的值是个只有一个元素的列表`['5']`，这个元素是字符串'5'。Python会把字符串'5'
  解析为True，所以整个表达式的值就等于or左侧那个子表达式的值，即`my_values.get('red', [''])[0]`。
* 对于green，这个键值也存在于my_value字典（dict）里面，它对应的值是个只有一个元素的列表`['']`
  ，这个元素是空白字符串。Python会把空白字符串解析为False，所以green变量的值就等于or右侧那个子表达式的值，也就是0。
* 对于opacity，这个键值不存在于my_value字典（dict）里面，get方法会返回传递给它的第二个值`['']`
  ，和green的情况类似，元素是空白字符串。Python会把空白字符串解析为False，所以opacity变量的值就等于or右侧那个子表达式的值，也就是0。

但是，上面的表达式可读性比较差，相比之下，改用if/else条件表达式，代码可读性会好一些。
```
>>> green_str = my_value.get('green', [''])
>>> if green_str[0]:
...     green = green_str[0]
... else:
...     green =0
... 
>>> green
0
```

如果要反复使用这套逻辑，建议写成辅助函数比较好，即使像上面这个例子一样只用三次。
```
>>> def get_first_value(value, key, default=0):
...     found = value.get(key, [''])
...     if found[0]:
...         return found[0]
...     return default
... 
>>> green = get_first_value(my_value, 'green')
>>> green
0
```


要点：
* Python的语法很容易把复杂的意思挤到同一行表达式里，这样写很难懂。
* 复杂的表达式，尤其是那种需要重复使用的复杂表达式，应该写到辅助函数里面。
* 用if/else结构写成的条件表达式，要比用or与and写成的Boolean表达式更好懂。
* 遵循循DRY原则，不要重复自己写过的代码（Don't Repeat Yourself）。




















