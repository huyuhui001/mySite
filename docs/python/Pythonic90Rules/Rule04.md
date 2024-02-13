# 第4条　用支持插值的f-string取代C风格的格式字符串与str.format方法

格式化（formatting）是指把数据填写到预先定义的文本模板里面，形成一条用户可读的消息，并把这条消息保存成字符串的过程。

用Python对字符串做格式化处理有四种办法可以考虑，这些办法都内置在语言和标准库里面。 但其中三种办法有严重的缺陷，现在先解释为什么不要使用这三种办法，最后再给出剩下的那一种。

Python里面最常用的字符串格式化方式是采用%格式化操作符(C风格的格式字符串)。 这个操作符左边的文本模板叫作格式字符串（format
string），我们可以在操作符右边写上某个值或者由多个值所构成的元组（tuple），用来替换格式字符串里的相关符号。

python字符串格式化符号：

* %c：字符及其ASCII码
* %s：字符串
* %d：整数
* %u：无符号整型
* %o：无符号八进制数
* %x：无符号十六进制数
* %X：无符号十六进制数（大写）
* %f：浮点数字，可指定小数点后的精度
* %e：用科学计数法格式化浮点数
* %E：作用同%e，用科学计数法格式化浮点数
* %g：%f和%e的简写
* %G：%f 和 %E 的简写
* %p：用十六进制数格式化变量的地址

```
a = 128
b = 3.1415926
print('Binary is %d, Hex is %X, Oct is %o, Float is %e' % (a, a, a, b))
>>>
Binary is 128, Hex is 80, Oct is 200, Float is 3.141593e+00
```

C风格的格式字符串，在Python里有四个缺点。

第一个缺点是，如果%右侧那个元组里面的值在类型或顺序上有变化，那么程序可能会因为转换类型时发生不兼容问题而出现错误。

```
>>> key = 'my_var'
>>> value = 1.234
>>> formatted = '%-10s = %.2f' % (key, value)  # %-10s代表=左边字串总长度10,不足部分在尾部添加空格
>>> formatted
'my_var     = 1.23'
>>> 
```

如果把key跟value互换位置，或者左侧那个格式字符串里面的两个说明符对调了顺序，那么程序就会在运行时出现异常。

```
>>> key = 'my_var'
>>> value = 1.234
>>> formatted = '%-10s = %.2f' % (value, key)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: must be real number, not str


>>> key = 'my_var'
>>> value = 1.234
>>> formatted = '%.2f = %-10s' % (key, value)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: must be real number, not str
```

第二个缺点是，在填充模板之前，经常要先对准备填写进去的这个值稍微做一些处理，但这样一来，整个表达式可能就会写得很长，影响程序的可读性。

```
>>> pantry = [
...     ('avocados', 1.25),
...     ('bananas', 2.5),
...     ('cherries', 15)
... ]
>>> for i, (item, count) in enumerate(pantry):
...     print(
...         '#%d: %-10s = %.2f' % (
...         i + 1,
...         item.title(),
...         round(count)
...         )
...     )
... 
#1: Avocados   = 1.00
#2: Bananas    = 2.00
#3: Cherries   = 15.00
```

第三个缺点是，如果想用同一个值来填充格式字符串里的多个位置，那么必须在%操作符右侧的元组中相应地多次重复该值。

```
>>> template = '%s loves food. See %s cook.'
>>> name = 'Max'
>>> formatted = template % (name, name)
>>> formatted
'Max loves food. See Max cook.'

```

为了解决上面提到的一些问题，Python的%操作符允许我们用dict取代tuple，解决了%操作符两侧的顺序不匹配问题。

```
>>> key = 'my_var'
>>> value = 1.234
>>> old_way = '%-10s = %.2f' % (key, value)
>>> new_way = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}  # 对应
>>> reordered = '%(key)-10s = %(value).2f' % {'value': value, 'key': key}  # 互换
>>> assert old_way == new_way == reordered
>>> old_way
'my_var     = 1.23'
>>> new_way
'my_var     = 1.23'
>>> reordered
'my_var     = 1.23'
```

用dict取代tuple，也解决用同一个值替换多个格式说明符的问题，我们就不用在%操作符右侧重复这个值了。

```
>>> name = 'Max'
>>> template = '%s loves food. See %s cook.'
>>> before = template % (name, name)
>>> template = '%(name)s loves food. See %(name)s cook.'
>>> after = template % {'name':  name}
>>> assert before == after
>>> before
'Max loves food. See Max cook.'
>>> after
'Max loves food. See Max cook.'
```

但是，这种写法会让第二个缺点变得更加严重，格式化表达式变得更加冗长，看起来也更加混乱。如下例：

```
>>> pantry = [
...     ('avocados', 1.25),
...     ('bananas', 2.5),
...     ('cherries', 15)
... ]
>>> for i, (item, count) in enumerate(pantry):
...     before = '#%d: %-10s = %.2f' % (
...         i + 1,
...         item.title(),
...         round(count)
...         )
...     after = '#%(loop)d: %(item)-10s = %(count).2f' % {
...         'loop': i + 1,
...         'item': item.title(),
...         'count': round(count)
...     }
...     assert before == after
...     print(before)
...     print(after)
... 
#1: Avocados   = 1.00
#1: Avocados   = 1.00
#2: Bananas    = 2.00
#2: Bananas    = 2.00
#3: Cherries   = 15.00
#3: Cherries   = 15.00
```

所以，第四个缺点是，把dict写到格式化表达式里面会让代码变多，每个键都至少要写两次。为了查看格式字符串中的说明符究竟对应于字典里的哪个键，必须在这两段代码之间来回跳跃。如果要对键名稍做修改，那么必须同步修改格式字符串里的说明符，这更让代码变得相当烦琐，可读性更差。

## 内置的format函数与str类的format方法

Python 3添加了高级字符串格式化（advanced stringformatting）机制，它的表达能力比老式C风格的格式字符串要强，且不再使用%操作符。

下面这段代码，演示了这种新的格式化方式。在传给format函数的格式里面，逗号表示显示千位分隔符，^表示居中对齐。

```
>>> a = 1234.5678
>>> formatted = format(a, ',.2f')
>>> formatted
'1,234.57'

>>> b = 'my string'
>>> formatted = format(b, '^20s')
>>> formatted
'     my string      '
```

如果str类型的字符串里面有许多值都需要调整格式，则可以把格式有待调整的那些位置在字符串里面先用{}代替，然后按从左到右的顺序，把需要填写到那些位置的值传给format方法，使这些值依次出现在字符串中的相应位置。

```
>>> key = 'my_var'
>>> value = 1.234
>>> formatted = '{} = {}'.format(key, value)
>>> formatted
'my_var = 1.234'
>>> formatted = '{} = {}'.format(value, key)
>>> formatted
'1.234 = my_var'
```

通过在{}里写个冒号，然后把格式说明符写在冒号的右边，来添加格式。（添加格式后，互换会报错）

```
>>> formatted = '{:<10} = {:.2f}'.format(key, value)
>>> formatted
'my_var     = 1.23'

>>> formatted = '{:<10} = {:.2f}'.format(value, key)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: Unknown format code 'f' for object of type 'str'
```

也可以给str的{}里面写上数字，用来指代format方法在这个位置所接收到的参数值位置索引。 以后即使这些{}在格式字符串中的次序有所变动，也不用调换传给format方法的那些参数。于是，这就避免了前面讲的第一个缺点所提到的那个顺序问题。

```
>>> key = 'my_var'
>>> value = 1.234
>>> formatted = '{} = {}'.format(key, value)
>>> formatted
'my_var = 1.234'

>>> formatted = '{1} = {0}'.format(key, value)
>>> formatted
'1.234 = my_var'

>>> formatted = '{2} = {1}'.format(key, value)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: Replacement index 2 out of range for positional args tuple
```

同一个位置索引可以出现在str的多个{}里面，这就不需要把这个值重复地传给format方法，于是就解决了前面提到的第三个缺点。

```
>>> name = 'Max'

>>> formatted = '%s loves food. See %s cook.' % (name, name)
>>> formatted
'Max loves food. See Max cook.'

>>> formatted = '%(name)s loves food. See %(name)s cook.' % {'name': name}
>>> formatted
'Max loves food. See Max cook.'

>>> formatted = '{0} loves food. See {0} cook.'.format(name)
>>> formatted
'Max loves food. See Max cook.'
```

上述功能分析：

* 系统先把str.format方法接收到的每个值传给内置的format函数，并找到这个值在字符串里对应的{}，同时将{}里面写的格式也传给format函数，例如系统在处理value的时候，传的就是format(value,'.2f')。
* 然后，系统会把format函数所返回的结果写在整个格式化字符串{}所在的位置。
* 另外，每个类都可以通过__format__这个特殊的方法定制相应的逻辑，这样的话，format函数在把该类实例转换成字符串时，就会按照这种逻辑来转换。

转义处理：

```
>>> formatted = '%.2f%%' % 12.5
>>> formatted
'12.50%'

>>> formatted = '{} replace {{}}'.format(1.23)
>>> formatted
'1.23 replace {}'
```

然而，str.format方法并没有解决上面讲的第二个缺点。如果在对值做填充之前要先对这个值做出调整，那么用这种方法写出来的代码还是跟原来一样乱，阅读性差。对比一下：

```
>>> pantry = [
...     ('avocados', 1.25),
...     ('bananas', 2.5),
...     ('cherries', 15)
... ]
>>> for i, (item, count) in enumerate(pantry):
...     before = '#%d: %-10s = %.2f' % (
...         i + 1,
...         item.title(),
...         round(count)
...         )
...     after = '#%(loop)d: %(item)-10s = %(count).2f' % {
...         'loop': i + 1,
...         'item': item.title(),
...         'count': round(count)
...     }
...     new_style = '#{}: {:<10s} = {:.2f}'.format(
...         i + 1,
...         item.title(),
...         round(count)
...     )
...     assert before == after == new_style
...     print(before)
...     print(after)
...     print(new_style)
... 
#1: Avocados   = 1.00
#1: Avocados   = 1.00
#1: Avocados   = 1.00
#2: Bananas    = 2.00
#2: Bananas    = 2.00
#2: Bananas    = 2.00
#3: Cherries   = 15.00
#3: Cherries   = 15.00
#3: Cherries   = 15.00
```

## 插值格式字符串f-string

Python 3.6添加了一种新的特性，叫作插值格式字符串（interpolated format string，简称f-string），可以解决上面提到的所有问题。

下面按照从短到长的顺序把这几种写法所占的篇幅对比一下，这样很容易看出符号右边的代码到底有多少。C风格的写法与采用str.format方法的写法可能会让表达式变得很长，但如果改用f-string，或许一行就能写完。

```
>>> key = 'my_var'
>>> value = 1.234
>>> f_string = f'{key:<10} = {value:.2f}'
>>> c_tuple = '%-10s = %.2f' % (key, value)
>>> str_args = '{:<10} = {:.2f}'.format(key, value)
>>> str_kw = '{key:<10} = {value:.2f}'.format(key=key, value=value)
>>> c_dict = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}

>>> assert c_tuple == c_dict == f_string
>>> assert str_args == str_kw == f_string

>>> f_string
'my_var     = 1.23'
>>> c_tuple
'my_var     = 1.23'
>>> str_args
'my_var     = 1.23'
>>> str_kw
'my_var     = 1.23'
>>> c_dict
'my_var     = 1.23'
```

对比下面，把str.format方法的写法改用f-string，一行就能写完。

```
>>> pantry = [
...     ('avocados', 1.25),
...     ('bananas', 2.5),
...     ('cherries', 15)
... ]
>>> for i, (item, count) in enumerate(pantry):
...     before = '#%d: %-10s = %.2f' % (
...         i + 1,
...         item.title(),
...         round(count)
...         )
...     after = '#%(loop)d: %(item)-10s = %(count).2f' % {
...         'loop': i + 1,
...         'item': item.title(),
...         'count': round(count)
...     }
...     new_style = '#{}: {:<10s} = {:.2f}'.format(
...         i + 1,
...         item.title(),
...         round(count)
...     )
...     f_string = f'#{i+1}: {item.title():<10s} = {round(count):.2f}'
...     assert before == after == new_style == f_string
...     print(before)
...     print(after)
...     print(new_style)
...     print(f_string)
... 
#1: Avocados   = 1.00
#1: Avocados   = 1.00
#1: Avocados   = 1.00
#1: Avocados   = 1.00
#2: Bananas    = 2.00
#2: Bananas    = 2.00
#2: Bananas    = 2.00
#2: Bananas    = 2.00
#3: Cherries   = 15.00
#3: Cherries   = 15.00
#3: Cherries   = 15.00
#3: Cherries   = 15.00
```

要点总结：

* 采用%操作符把值填充到C风格的格式字符串时会遇到许多问题，而且这种写法比较烦琐。
* str.format方法专门用一套迷你语言来定义它的格式说明符，这套语言给我们提供了一些有用的概念，但是在其他方面，这个方法还是存在与C风格的格式字符串一样的多种缺点，所以我们也应该避免使用它。
* f-string采用新的写法，将值填充到字符串之中，解决了C风格的格式字符串所带来的最大问题。
* f-string是个简洁而强大的机制，可以直接在格式说明符里嵌入任意Python表达式。



