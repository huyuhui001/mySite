# 第8条　用zip函数同时遍历两个迭代器

写Python代码时，经常会根据某份列表中的对象创建许多与这份列表有关的新列表。

下面这样的列表推导机制，可以把表达式运用到源列表的每个元素上面，从而生成一份派生列表（参见Rule27）。

```
>>> names = ['Cecilia', 'Lise', 'Marie']
>>> counts = [len(n) for n in names]
>>> counts
[7, 4, 5]
```

派生列表中的元素与源列表中对应位置上面的元素有着一定的关系。如果想同时遍历这两份列表，那可以根据源列表的长度做迭代。

```
>>> names = ['Cecilia', 'Lise', 'Marie']
>>> longest_name = None
>>> max_count = 0
>>> counts = [len(n) for n in names]
>>> for i in range(len(names)):
...     count = counts[i]
...     if count > max_count:
...         longest_name = names[i]
...         max_count = count
... 
>>> longest_name
'Cecilia'
```

用enumerate来改写上面的代码，改善上面代码中复杂的循环关系。

```
>>> names = ['Cecilia', 'Lise', 'Marie']
>>> longest_name = None
>>> max_count = 0
>>> counts = [len(n) for n in names]
>>> for i, name in enumerate(names):
...     count = counts[i]
...     if count > max_count:
...         longest_name = name
...         max_count = count
... 
>>> longest_name
'Cecilia'
```

用zip来改写代码，使之更简洁。 zip函数能把两个或更多的iterator封装成惰性生成器（lazy generator）。 每次循环时，它会分别从这些迭代器里获取各自的下一个元素，并把这些值放在一个元组里面。
zip每次只从它封装的那些迭代器里面各自取出一个元素，所以即便源列表很长，程序也不会因为占用内存过多而崩溃。 而这个元组可以拆分到for语句里的那些变量之中（参见Rule06）。
这样写出来的代码，比通过下标访问多个列表的那种代码要清晰得多。

```
>>> names = ['Cecilia', 'Lise', 'Marie']
>>> longest_name = None
>>> max_count = 0
>>> counts = [len(n) for n in names]
>>> for name, count in zip(names, counts):
...     if count > max_count:
...         longest_name = name
...         max_count = count
... 
>>> longest_name
'Cecilia'
```

但是，如果输入zip的那些列表的长度不一致，用zip同时遍历那些列表，会产生奇怪的结果。 例如，我给names列表里又添加了一个名字，但是忘了把它的长度更新到counts列表之中。 新添加的那个'Rosalind'
元素不会被打印出来，因为zip函数在执行中，只要其中任何一个迭代器处理完毕，它就不再往下走了。 于是，循环的次数实际上等于最短的那份列表所具备的长度。

一般情况下，我们都是根据某份列表推导出其他几份列表，然后把这些列表一起封装到zip里面，并保证这些列表长度相同。

```
>>> names.append('Rosalind')
>>> names
['Cecilia', 'Lise', 'Marie', 'Rosalind']
>>> for name, count in zip(names, counts):
...     print(name)
... 
Cecilia
Lise
Marie
```

在列表长度不同的情况下，如果无法确定这些列表的长度相同，那就不要把它们传给zip，而是应该传给另一个叫作zip_longest的函数，这个函数位于内置的itertools模块里。
如果其中有些列表已经遍历完了，那么zip_longest会用当初传给fillvalue参数的那个值来填补空缺（本例中空缺的为字符串'Rosalind'的长度值），默认的参数值是None。

```
>>> import itertools
>>> names = ['Cecilia', 'Lise', 'Marie']
>>> longest_name = None
>>> max_count = 0
>>> counts = [len(n) for n in names]
>>> names.append('Rosalind')
>>> names
['Cecilia', 'Lise', 'Marie', 'Rosalind']
>>> counts
[7, 4, 5]
>>> for name, count in itertools.zip_longest(names, counts):
...     print(f'{name}: {count}')
... 
Cecilia: 7
Lise: 4
Marie: 5
Rosalind: None
```

要点：

* 内置的zip函数可以同时遍历多个迭代器。
* zip会创建惰性生成器，让它每次只生成一个元组，所以无论输入的数据有多长，它都是一个一个处理的。
* 如果提供的迭代器的长度不一致，那么只要其中任何一个迭代完毕，zip就会停止。
* 如果想按最长的那个迭代器来遍历，那就改用内置的itertools模块中的zip_longest函数。




