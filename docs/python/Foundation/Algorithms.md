# 数据结构和算法

## 大O记法

算法分析是一种独立于实现的算法度量方法。

数量级（order of magnitude）常被称作大O记法（O指order），记作O(f(n))。它提供了步骤数的一个有用的近似方法。f(n)函数为T(n)函数中起决定性作用的部分提供了简单的表示。

大O记法使得算法可以根据随问题规模增长而起主导作用的部分进行归类。

### 异序词检测问题。

如果一个字符串只是重排了另一个字符串的字符，那么这个字符串就是另一个的异序词。

方案1：清点法

清点第1个字符串的每个字符，看看它们是否都出现在第2个字符串中。
在字符列表中检查第1个字符串中的每个字符，如果找到了，就替换掉。

这个方案的时间复杂度是O(n^2)。
```
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
```
allotropyWord_1('hello', 'olleh')
```
注意list_a的变化过程(匹配到即替换None)。
```
['o', 'l', 'l', 'e', None]
['o', 'l', 'l', None, None]
['o', None, 'l', None, None]
['o', None, None, None, None]
[None, None, None, None, None]
```

方案2：排序法

按照字母表顺序给字符排序，异序词得到的结果将是同一个字符串。

这个方案的时间复杂度是O(n^2)。
```
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
```
allotropyWord_2('hello', 'olleh')
```

方案3：计数法

两个异序词有同样数目的a、同样数目的b、同样数目的c，等等。
使用26个计数器，对应每个字符。每遇到一个字符，就将对应的计数器加1。
如果两个计数器列表相同，那么两个字符串肯定是异序词。

这个方案的时间复杂度是O(n)。
```
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
```
allotropyWord_3('hello', 'olleh')
```


!!! Reference
    [Python的时间复杂度(Time Complexity)](https://wiki.python.org/moin/TimeComplexity)









