# Python数据结构和算法

参考书目：

* "Problem Solving with Algorithms and Data Structures Using Python (Second Edition)" by Bradley N.Miller and David L.Ranum.

## 大O记法

算法分析是一种独立于实现的算法度量方法。

数量级（order of magnitude）常被称作大O记法（O指order），记作O(f(n))。它提供了步骤数的一个有用的近似方法。f(n)函数为T(n)函数中起决定性作用的部分提供了简单的表示。

大O记法使得算法可以根据随问题规模增长而起主导作用的部分进行归类。

### 异序词检测问题

如果一个字符串只是重排了另一个字符串的字符，那么这个字符串就是另一个的异序词。

方案1：清点法

清点第1个字符串的每个字符，看看它们是否都出现在第2个字符串中。
在字符列表中检查第1个字符串中的每个字符，如果找到了，就替换掉。

这个方案的时间复杂度是O(n^2)。

```python
def allotropyWord_1(s1, s2):
    list_a = list(s2)
    
    pos1 = 0
    stillOK = True

    while pos1 < len(s1) and stillOK:
        pos2 = 0
        found = False
        
        while pos2 < len(list_a) and not found:
            if s1[pos1] == list_a[pos2]:
                found = True
            else:
                pos2 = pos2 + 1
        
        if found:
            list_a[pos2] = None
        else:
            stillOK = False
        
        pos1 = pos1 + 1
    
    return stillOK
```

运行：

```python
allotropyWord_1('hello', 'olleh')
```

注意list_a的变化过程(匹配到即替换None)。

```python
['o', 'l', 'l', 'e', None]
['o', 'l', 'l', None, None]
['o', None, 'l', None, None]
['o', None, None, None, None]
[None, None, None, None, None]
```

方案2：排序法

按照字母表顺序给字符排序，异序词得到的结果将是同一个字符串。

这个方案的时间复杂度是O(n^2)。

```python
def allotropyWord_2(s1, s2):
    list1 = list(s1)
    list2 = list(s2)

    list1.sort()
    list2.sort()

    pos = 0
    matched = True

    while pos < len(s1) and matched:
        if list1[pos] == list2[pos]:
            pos = pos + 1
        else:
            matched = False

    return matched
```

运行：

```python
allotropyWord_2('hello', 'olleh')
```

方案3：计数法

两个异序词有同样数目的a、同样数目的b、同样数目的c，等等。
使用26个计数器，对应每个字符。每遇到一个字符，就将对应的计数器加1。
如果两个计数器列表相同，那么两个字符串肯定是异序词。

这个方案的时间复杂度是O(n)。

```python
def allotropyWord_3(s1, s2):
    c1 = [0] * 26
    c2 = [0] * 26

    for i in range(len(s1)):  # 每个字符的ASCII码与字符a的ASCII码的差值(偏移量)
        pos = ord(s1[i]) - ord('a')
        c1[pos] = c1[pos] + 1

    for i in range(len(s2)):
        pos = ord(s2[i]) - ord('a')
        c2[pos] = c2[pos] + 1

    j = 0
    stillOK = True

    while j < 26 and stillOK:
        if c1[j] == c2[j]:
            j = j + 1
        else:
            stillOK = False
    
    return stillOK
```

运行：

```python
allotropyWord_3('hello', 'olleh')
```

参考：

* [Python的时间复杂度(Time Complexity)](https://wiki.python.org/moin/TimeComplexity)

## 线性数据结构

真正区分线性数据结构的是元素的添加方式和移除方式，尤其是添加操作和移除操作发生的位置。

### 栈

栈有时也被称作“下推栈”。它是有序集合，添加操作和移除操作总发生在同一端，即“顶端”，另一端则被称为“底端”。

最新添加的元素将被最先移除。这种排序原则被称作LIFO（last-in first-out），即后进先出。

栈的反转特性。

栈的实现方法1:

`append()`和`pop()`的时间复杂度都是O(1)，所以不论栈中有多少个元素，`push`操作和`pop`操作都会在恒定的时间内完成。

```python
class Stack():
    def __init__(self) -> None:
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[len(self.items) - 1]
    
    def size(self):
        return len(self.items)
```

栈的实现方法2:

`insert(0)`和`pop(0)`的时间复杂度都是O(n)，元素越多就越慢，性能则受制于栈中的元素个数。

```python
class Stack():
    def __init__(self) -> None:
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.insert(0, item)
    
    def pop(self):
        return self.items.pop(0)
    
    def peek(self):
        return self.items[0]
    
    def size(self):
        return len(self.items)
```

对上面的实现，可以通过下面进行分别验证：

```python
s = Stack()
s.isEmpty()
s.push(3)
s.push('dog')
s.peek()
s.size()
s.isEmpty()
s.push(6.6)
s.pop()
s.size()
```

#### 括号匹配问题

```python
#!/usr/bin/python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Stack():
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[len(self.items) - 1]
    
    def size(self):
        return len(self.items)


# 关联左右括号
def matches(open, close):
    opens = "([{"
    closers = ")]}"
    # 符合关联的，返回True
    return opens.index(open) == closers.index(close)


def parChecker(symbolString):
    s = Stack()

    matched = True
    index = 0
    
    # 读取输入字串每个字符
    while index < len(symbolString) and matched:
        symbol = symbolString[index]
        
        if symbol in "([{":  # 左括号入栈
            s.push(symbol)
        else:
            if s.isEmpty():  # 遇到非左括号字符，如为空，则退出循环
                matched = False
            else:
                top = s.pop()  # 遇到非左括号字符，如不为空，则出栈，并判断是否未为对应的右括号
                if not matches(top, symbol):  # 否则退出循环
                    matched = False
        
        index = index + 1
    
    # 完成每个字符的出入栈检查，当前栈为空，且都匹配，则返回True
    if matched and s.isEmpty():
        return True
    else:
        return False


if __name__ == '__main__':
    parChecker("([[{}])")
    parChecker("([{}])")

```

执行结果如下，符合预期。

```python
False
True
```

#### 进制转换问题

例如，使用“除以2”的算法，十进制数转换成二进制数，利用栈来保存二进制结果的每一位。

“除以2”算法假设待处理的整数大于0。
它用一个简单的循环不停地将十进制数除以2，并且记录余数。
第一次除以2的结果能够用于区分偶数和奇数。
如果是偶数，则余数为0，因此个位上的数字为0；
如果是奇数，则余数为1，因此个位上的数字为1。
可以将要构建的二进制数看成一系列数字；计算出的第一个余数是最后一位。
这体现了反转特性，因此适用栈来处理。

```python
class Stack():
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[len(self.items) - 1]
    
    def size(self):
        return len(self.items)


def decConverter(decNumber, baseNumber):
    remstack = Stack()
    digits = "0123456789ABCDEF"

    while decNumber > 0:
        rem = decNumber % baseNumber
        remstack.push(rem)
        decNumber = decNumber // baseNumber
    
    newString = ""

    while not remstack.isEmpty():
        newString = newString + digits[remstack.pop()]
    
    return newString


if __name__ == '__main__':
    decConverter(233, 2)
    decConverter(233, 8)
    decConverter(233, 10)
    decConverter(233, 16)
```

运行结果：

```python
'11101001'
'351'
'233'
'E9'
```

### 队列

使用`insert()`向队列的尾部添加新元素，时间复杂度是O(n)。
使用`pop()`移除队列头部的元素（列表中的最后一个元素），时间复杂度是O(1)。

```python
class Queue():
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        return self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)


if __name__ == '__main__':
    q = Queue()
    q.isEmpty()
    q.enqueue(2)
    q.enqueue('h')
    q.size()
    q.isEmpty()
    q.dequeue()
    q.size()
```

运行结果:

```python
True
2
False
2
1
```

#### 约瑟夫斯问题

通过模拟实现传土豆游戏来解释约瑟夫斯问题。

```python
class Queue():
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        return self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)


def hotPotato(namelist, num):
    simqueue = Queue()

    for name in namelist:
        simqueue.enqueue(name)
    
    while simqueue.size() > 1:
        for i in range(num):
            simqueue.enqueue(simqueue.dequeue())
        
        simqueue.dequeue()

    return simqueue.dequeue()


if __name__ == '__main__':
    hotPotato(["Bill", "David", "Susan", "Jane", "Ken", "Brad"], 7)

 ```

 运行结果如下，最后只剩Susan。设定不同的num（这里是7）会得到不同的结果。

 ```python
'Susan'
 ```

#### 打印任务

### 双端队列

### 列表
