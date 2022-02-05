# 第3条　了解bytes与str的区别

## UNICODE编码简介

ASCII编码规定1个字节等于8个比特位，代表1个字符的编码，除了第一位是0， 其他7位都可以有0 或者 1 两个选择，所以ASCII 一共可以表示 2^7 ，也就是128个字符。包括a-z 大小写，0-9 数字
和一些标点符号等。其中真正可读的只有95 个字符，其他的都是一些控制符，比如NUL，代表NULL。

多字节编码，比如双字节编码方式，BIG-5和GB18030包含了大多数中文简体和繁体。这个编码不兼容ASCII，同时还占用较多的空间和内存。

UNICODE不是一种编码， 而是定义了一个表， 表中为世界上每种语言中的每个字符设定了统一并且唯一的码位 （code point），以满足跨语言、跨平台进行文本转换的要求。

UTF-8编码规定英文字母系列用1个字节表示，汉字用3个字节表示等等。UTF-8的特点是对不同范围的字符使用不同长度的编码。 下表表示如何从一个从Unicode 转化到UTF-8 ,
对于前0x7F的字符，UTF-8编码和ASCII码是一一对应的。 如果一个字符在000800-00FFFF 之间，那转化到UTF-8 需要用三字节模板，使用16个码位，每个x就是一个码位。

| Unicode编码（十六进制） | UTF-8字节流（二进制）                 |
|----------------------|-------------------------------------|
| 000000 - 00007F      | 0xxxxxxx                            |
| 000080 - 0007FF      | 110xxxx 10xxxxxx                    |
| 000800 - 00FFFF      | 1110xxxx 10xxxxxx 10xxxxxx          |
| 010000 - 10FFFF      | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx |

Python有两种类型可以表示字符序列(sequence)：一种是bytes，另一种是str。

* bytes实例包含的是原始数据，即8位的无符号值（通常按照ASCII编码标准来显示）。
* str实例包含的是Unicode码点（code point，也叫作代码点），这些码点与人类语言之中的文本字符相对应。

```
>>> a = b'h\x65llo'
>>> a
b'hello'
>>> list(a)
[104, 101, 108, 108, 111]

>>> b = 'a\u0300 hello'
>>> b
'à hello'
>>> list(b)
['a', '̀', ' ', 'h', 'e', 'l', 'l', 'o']
```

内存是unicode编码格式，硬盘是utf-8。 在做编码转换时候，通常用unicode作为中间编码。 先将其他编码的字符串解码(decode)成unicode,再从unicode编码(encode)成另一种编码格式。
decode的作用是将二进制数据解码成unicode编码。 encode的作用是将unicode编码的字符串编码成二进制数据。

要把Unicode数据转换成二进制数据，必须调用str的encode方法。 要把二进制数据转换成Unicode数据，必须调用bytes的decode方法。
调用这些方法的时候，可以明确指出自己要使用的编码方案，也可以采用系统默认的方案，通常是指UTF-8。 在bytes和str的互相转换过程中，实际就是编码解码的过程，必须显式地指定编码格式。

```
>>> s = '中文'
>>> s
'中文'
>>> type(s)
<class 'str'>

>>> b = bytes(s, encoding='utf-8')
>>> b
b'\xe4\xb8\xad\xe6\x96\x87'
>>> type(b)
<class 'bytes'>

>>> s.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'

>>> b.decode('utf-8')
'中文'
>>> 
>>> str(b, encoding='utf-8')
'中文'
```

编写Python程序的时候，一定要把解码和编码操作放在界面最外层来做，让程序的核心部分可以使用Unicode数据来运作，这种办法通常叫作Unicode三明治（Unicode sandwich）。

我们可以编写辅助函数来确保程序收到的字符序列确实是期望要操作的类型（要知道自己想操作的到底是Unicode码点，还是原始的8位值。用UTF-8标准给字符串编码，得到的就是这样的一系列8位值）。

辅助函数to_str接受bytes或str实例，并返回str：

```
>>> def to_str(bytes_or_str):
...     if isinstance(bytes_or_str, bytes):
...         value = bytes_or_str.decode('utf-8')
...     else:
...         value = bytes_or_str
...     return value
... 
>>> repr(to_str(b'foo'))
"'foo'"
>>> repr(to_str('foo'))
"'foo'"
>>> to_str('foo')
'foo'
>>> to_str(b'foo')
'foo'
```

辅助函数to_bytes接受bytes或str实例，并返回bytes：

```
>>> def to_bytes(bytes_or_str):
...     if isinstance(bytes_or_str, str):
...         value = bytes_or_str.encode('utf-8')
...     else:
...         value = bytes_or_str
...     return value
... 
>>> repr(to_bytes(b'foo'))
"b'foo'"
>>> repr(to_bytes('foo'))
"b'foo'"
>>> to_bytes(b'foo')
b'foo'
>>> to_bytes('foo')
```

bytes与str这两种实例不能在某些操作符（例如>、==、+、%操作符）上面混用。

```
>>> b'one' + b'two'
b'onetwo'
>>> 'one'+'two'
'onetwo'
```

不能将str实例添加到bytes实例：

```
>>> b'one' + 'two'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't concat str to bytes
```

不能将byte实例添加到str实例：

```
> > > 'one' + b'two'
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "bytes") to str
```

str实例不能与bytes实例比较，即便这两个实例表示的字符完全相同，它们也不相等：

```
>>> assert 'red' >= b'red'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '>=' not supported between instances of 'str' and 'bytes'

>>> assert b'red' >= 'red'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '>=' not supported between instances of 'bytes' and 'str'
```

两种类型的实例都可以出现在%操作符的右侧，用来替换左侧那个格式字符串（format string）里面的%s。

```
>>> print(b'red %s' % b'blue')
b'red blue'
>>> print('red %s' % 'blue')
red blue
```

如果格式字符串是bytes类型，那么不能用str实例来替换其中的%s。 如果格式字符串是str类型，则可以用bytes实例来替换其中的%s。(系统在bytes实例上面调用__repr__
方法（Rule75），然后用这次调用所得到的结果替换格式字符串里的%s，因此程序会直接输出b'blue'，而不是输出blue本身。)

```
>>> print(b'red %s' % 'blue')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: %b requires a bytes-like object, or an object that implements __bytes__, not 'str'

>>> print('red %s' % b'blue')
red b'blue'
```

在操作文件句柄的时候，这里的句柄指由内置的open函数返回的句柄。这样的句柄默认需要使用Unicode字符串操作，而不能采用原始的bytes。

从文件中读取二进制数据（或者把二进制数据写入文件）时，应该用'rb'（'wb'）这样的二进制模式打开文件。

```
>>> with open('./temp/data.bin', 'w') as f:
...     f.write(b'\xf1\xf2\xf3\xf4\xf5')
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: write() argument must be str, not bytes
>>> 
>>> with open('./temp/data.bin', 'wb') as f:
...     f.write(b'\xf1\xf2\xf3\xf4\xf5')
... 
5
>>>
```

```
>>> with open('./temp/data.bin', 'r') as f:
...     data = f.read()
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/usr/local/lib/python3.9/codecs.py", line 322, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1 in position 0: invalid continuation byte
>>> 
>>> 
>>> with open('./temp/data.bin', 'rb') as f:
...     data = f.read()
... 
>>> assert data == b'\xf1\xf2\xf3\xf4\xf5'
>>> 
```

如果要从文件中读取（或者要写入文件之中）的是Unicode数据，那么必须注意系统默认的文本编码方案。若无法肯定，可通过encoding参数明确指定。

```
>>> with open('./temp/data.bin', 'r', encoding='cp1252') as f:
...     data = f.read()
... 
>>> assert data == b'\xf1\xf2\xf3\xf4\xf5'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

查看当前操作系统默认的编码标准

```
>>> import locale
>>> locale.getpreferredencoding()
'UTF-8'
>>> 
```





