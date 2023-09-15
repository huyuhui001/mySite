# 5.接口、实现和多态

目标：

- 为给定的多项集类型开发接口；
- 按照多项集类型的接口实现多个类；
- 对给定多项集类型的不同实现评估运行时和内存使用情况的权衡；
- 实现一个简单的迭代器；
- 使用方法对包和集合进行操作；
- 判断包或集合是否适合在给定的应用程序里使用；
- 将包的实现转换成有序包的实现。

## 5.1.开发接口

### 5.1.1.设计包接口

### 5.1.2.指定参数和返回值

## 5.2.构造函数和类的实现

### 5.2.1.前置条件、后置条件、异常和文档

### 5.2.2.在Python里编写接口

练习题
1．包里的元素是有序的，还是无序的？

2．哪些操作会出现在所有多项集的接口里？

3．哪个方法负责创建多项集对象？

4．请说出接口与实现分离的3个原因。

## 5.3.开发基于数组的实现

### 5.3.1.选择并初始化数据结构

### 5.3.2.先完成简单的方法

### 5.3.3.完成迭代器

### 5.3.4.完成使用迭代器的方法

### 5.3.5.in运算符和__contains__方法

### 5.3.6.完成remove方法

### 5.3.7.练习题

1．解释多项集类的__init__方法的作用。

2．为什么调用方法比直接在类里引用实例变量更好？

3．对于ArrayBag的__init__方法，展示如何通过调用clear方法来简化代码。

4．解释为什么__iter__方法可能会是多项集类里最有用的方法。

5．解释为什么在ArrayBag类中不用包含__contains__方法。

## 5.4.开发基于链接的实现

### 5.4.1.初始化数据结构

### 5.4.2.完成迭代器

### 5.4.3.完成clear和add方法

### 5.4.4.完成remove方法

### 5.4.5.练习题

1．假设a是一个数组包，b是一个链接包，它们都不包含任何元素。请描述在这种情况下它们在内存使用上的差异。

2．为什么链接包仍然需要一个单独的实例变量来记录它的逻辑尺寸？

3．为什么从链接包里删除元素之后，程序员不用担心出现内存浪费的情况？

## 5.5.两种包实现的运行时性能

## 5.6.测试包的两种实现

## 5.7.使用UML绘制包资源

## 5.8.小结

- 接口是用户的软件资源可以使用的一组操作。
- 接口里的元素是函数和方法的定义以及它们的文档。
- 前置条件是指在函数或方法可以正确完成任务之前必须要满足的条件。
- 后置条件是指在函数或方法正确完成任务之后必须为真的条件。
- 设计良好的软件系统会把接口和它的实现分开。
- 实现是指满足接口的函数、方法或类。
- 多项集类型可以通过接口进行指定。
- 多项集类型可以有几个不同的实现类。
- 多态是指在两个或多个实现里使用相同的运算符、函数名称或方法名称。多态函数的示例是`str`和`len`；多态运算符的示例是`+`和`==`；多态方法的示例包括add和`isEmpty`。
- 包多项集类型是无序的，并且支持添加、删除和访问其元素等操作。
- 类图是一种描述类与类之间关系的可视化表示方法。
- 组合表示两个类之间整体与局部的关系。
- 聚合表示两个类之间一对多的关系。
- UML是一种描述软件资源之间关系的可视化表示方法。

## 5.9.复习题

1．包是：

- 线性多项集
- 无序多项集

2．用来设置对象实例变量的初始状态的方法是：

- `__init__`方法
- `__str__`方法

3．让程序员可以访问多项集里所有元素的方法是：

- `__init__`方法
- `__iter__`方法

4．改变对象内部状态的方法是：

- 访问器方法
- 变异器方法

5．一组可以被类的客户端使用的方法集称为：

- 实现
- 接口

6．多态用来代表的术语是：

- 多个类里相同的方法名称
- 用来存储另一个类里所包含数据的类

7．组合是指：

- 两个类之间部分与整体关系
- 两个类之间多对一关系

8．包中add方法的平均运行时为：

- `O(n)`
- `O(k)`

9．包中remove方法的平均运行时为：

- `O(n)`
- `O(k)`

10．在什么情况下，数组包实现会比链接包实现使用更少的内存：

- 含有少于一半的数据
- 含有一半以上的数据

## 5.10.编程练习

1．对于两个包实现，确定`==`操作的运行时。可以预见到，这里有几种情况需要分析。

2．对于包的两个实现，确定`+`运算符的运行时。

3．编码`ArrayBag`里`add`方法的代码，从而可以在需要的时候对数组尺寸进行调整。

4．编码`ArrayBag`里`remove`方法的代码，从而可以在需要的时候对数组尺寸进行调整。

5．在`ArrayBag`和`LinkedBag`类里添加`clone`方法。这个方法在调用的时候，不会接收任何参数，并且会返回当前包类型的一个完整副本。在下面这段代码的最后，变量`bag2`将包含数字`2`、`3`和`4`。

```python
bag1 = ArrayBag([2,3,4])
bag2 = bag1.clone()
bag1 == bag2    # Returns True
bag1 is bag2    # Returns False
```

6．集合是一个无序多项集，并且和包具有相同的接口。但是在集合里，元素是唯一的，而包里可以包含重复的物品。定义一个基于数组的叫作`ArraySet`的多项集新类。如果集合里的元素已经存在了，那么`add`方法将会忽略这个元素。

7．使用链接节点定义一个叫作`LinkedSet`的多项集新类来实现集合类型。如果集合里的元素已经存在了，那么`add`方法将会忽略这个元素。

8．有序包的行为和普通包的是一样的，但是它能够让用户在使用`for`循环时按照升序访问里面的元素。因此，添加到这个包类型里的元素，都必须具有一定的顺序并且支持比较运算符。这种类型元素的简单例子是：字符串和整数。定义一个支持这个功能的叫作`ArraySortedBag`的新类。和`ArrayBag`一样，这个新类会基于数组，但是它的`in`操作现在可以在对数时间里运行。要完成这一点，`ArraySortedBag`必须将新添加的元素按照顺序放到数组里。最简单的办法是修改`add`方法，从而让新元素插入适当的位置；然后，添加_`_contains__`方法来提供新的且更有效的搜索；最后，要把对`ArrayBag`的所有引用都替换为`ArraySortedBag`。（提示：把代码从`ArrayBag`类中复制到一个新文件里，然后在这个新文件里开始修改。）

9．确定`ArraySortedBag`里`add`方法的运行时。

10．Python的`for`循环可以让程序员在循环迭代多项集的时候对它执行添加或删除元素的操作。一些设计人员担心在迭代过程中对多项集的结构进行修改可能会导致程序崩溃。有一种修改策略是通过禁止在迭代期间对多项集进行变异来让`for`循环成为只读。你可以通过对变异操作进行计数，并且判断这个计数有没有在多项集的`__iter__`方法的任意节拍中被增加来检测这种类型的变异。当发生这种情况时，就可以引发异常从而避免计算的继续进行。把这个机制添加到`ArrayBag`类里。可以添加一个叫作`modCount`的新实例变量，这个实例变量会在`__init__`方法里设置为`0`；然后，每个变异器方法都会递增这个变量；最后，`__iter__`方法有一个叫作`modCount`的临时变量，这个临时变量的初始值是实例变量`self.modCount`的值。在`__iter__`方法里返回一个元素后，如果这两个修改过的计数器值不相等，就立即引发异常。用一个程序来测试你的修改，从而保证满足相应的需求。