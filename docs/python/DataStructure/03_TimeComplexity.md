# 搜索、排序以及复杂度分析

算法描述了一个随着问题被解决而停止的计算过程。

算法是计算机程序的基本组成部分之一，另一个基本组成部分是数据结构。

在算法执行过程中会消耗两个资源：处理对象所需的时间和空间（也就是内存）。对于算法来说，总会追求消耗更短的时间和占用更少的空间。在选择算法时，通常在空间/时间之间进行权衡。

算法质量的主要评估标准：

- 正确性，即算法能够真正解决所针对的问题；
- 可读性和易于维护性；
- 运行时性能；

目标：

- 根据问题的规模确定算法工作量的增长率；
- 使用大O表示法来描述算法的运行时和内存使用情况；
- 认识常见的工作量增长率或复杂度的类别（常数、对数、线性、平方和指数）；
- 将算法转换为复杂度低一个数量级的更快的版本；
- 描述顺序搜索算法和二分搜索算法的工作方式；
- 描述选择排序算法和快速排序算法的工作方式。

## 衡量算法的效率

衡量算法时间成本的两种方法：

- 用计算机时钟得到算法实际的运行时。这个过程被称为基准测试（benchmarking）或性能分析（profiling）。预测算法执行的抽象工作量依赖于特定的硬件或软件平台。
- 在不同问题规模下，统计需要执行的指令数。预测算法执行的抽象工作量适用于不同的硬件或软件平台。

### 3.1.1.衡量算法的运行时

```python
import time

problemSize = 10000000
print("%12s%16s" % ("Problem Size", "Seconds"))

for count in range(5):
    """
    在一个循环中，将问题规模翻倍5次，记录算法每次运行时间。
    """
    start = time.time()
    # 算法开始
    work = 1
    for x in range(problemSize):
        work += 1
        work -= 1
    # 算法结束
    elapsed = time.time() - start
    print("%12d%16.3f" % (problemSize, elapsed))
    problemSize *= 2

# 运行结果：
# Problem Size         Seconds
#     10000000           0.689
#     20000000           1.367
#     40000000           2.644
#     80000000           5.296
#    160000000          10.622
```

上述测试程序使用了`time`模块里的`time()`函数来记录运行时，即`time.time()`。这个函数会返回计算机的当前时间和1970年1月1日［也称为纪元（epoch）］相差的秒数。两次调用`time.time()`的结果之间的差值就代表了中间经历了多少秒。

上述测试程序在每次循环的时候都会执行两个扩展的赋值语句，也就是每次都执行的工作量是固定的，会消耗了一定的时间。

修改上述算法，我们可以从下面的运行结果看出，当`problemSize`为`1,000`时，算法的消耗时间就已经超过了原先算法，我们可以推断出继续测试`problemSize`为`10,000,000`的耗时已经变得不实际了。

```python
import time

problemSize = 1000
print("%12s%16s" % ("Problem Size", "Seconds"))
for count in range(5):
    start = time.time()
    # 算法开始
    work = 1
    for x in range(problemSize):
        for y in range(problemSize):
            work += 1
            work -= 1
    # 算法结束
    elapsed = time.time() - start
    print("%12d%16.3f" % (problemSize, elapsed))
    problemSize *= 2

# 运行结果：
# Problem Size         Seconds
#         1000           0.093
#         2000           0.350
#         4000           1.280
#         8000           5.004
#        16000          20.020
```

- 不同的硬件平台会有不同的处理速度，算法的运行时会因机器的不同而存在差异。
- 程序的运行时也会随着它和硬件之间的操作系统类型的不同而变化。
- 不同的编程语言和编译器生成的代码的性能也会有所不同，因此，在某一个硬件或软件平台上测得的运行时结果通常不能用来预测在其他平台上的性能。
- 用非常大的数据集确定算法的运行时是非常不切实际的。对于某些算法来说，不论是编译的代码还是硬件处理器的速度有多快，都没有任何的区别，因为它们在任何计算机上都没办法处理非常大的数据集。

### 3.1.2.统计指令数

统计指令数时，统计的是编写算法的高级语言里的指令数，而不是可执行机器语言程序里的指令数。

通过这种方式对算法进行分析时，把它分成两个部分：

- 无论问题的规模如何变化，指令执行的次数总是相同的；我们忽略这种类型，因为分析效率时它们的作用并不明显。
- 执行的指令数随着问题规模的变化而变化；我们重点关注这种类型，这种类型的指令通常可以在循环或者递归函数里找到。

我们来改写上面的例子，从统计运行时间变为统计迭代次数。

下面的算法中，迭代次数和问题规模是相等的。

```python
import time

problemSize = 10000000
print("%12s%16s" % ("Problem Size", "Seconds"))
for count in range(5):
    number = 0
    # 算法开始
    work = 1
    for x in range(problemSize):
        number += 1
        work += 1
        work -= 1
    # 算法结束
    print("%12d%16.3f" % (problemSize, Iterations))
    problemSize *= 2

# 运行结果：
# Problem Size      Iterations
#     10000000    10000000.000
#     20000000    20000000.000
#     40000000    40000000.000
#     80000000    80000000.000
#    160000000   160000000.000
```

下面的算法中，迭代次数和问题规模的平方。这就解释了为什么下面这个算法的耗时非常大。

```python
import time

problemSize = 1000
print("%12s%16s" % ("Problem Size", "Seconds"))
for count in range(5):
    number = 0
    # 算法开始
    work = 1
    for x in range(problemSize):
        for y in range(problemSize):
            number += 1
            work += 1
            work -= 1
    # 算法结束
    print("%12d%16.3f" % (problemSize, number))
    problemSize *= 2

# 运行结果：
# Problem Size      Iterations
#         1000     1000000.000
#         2000     4000000.000
#         4000    16000000.000
#         8000    64000000.000
#        16000   256000000.000
```

在下面的斐波那契递归的例子中，函数`fib(problemSize, counter)`中`counter`参数是一个对象，每次递归调用的时候，都会创建一个新的计数器对象。

从下面的运行结果可以看出，随着问题规模（Problem Size）的翻倍，指令数（递归调用的次数）在一开始的时候缓慢增长，随后迅速加快。

统计指令数是正确的思路，但以这种方式进行跟踪计数的问题在于，对于某些算法来说，如果问题规模非常大，计算机无法以足够快的速度运行，并在一定时间内得到结果。

```python
class Counter(object):
    """Models a counter."""

    # Class variable
    instances = 0

    #Constructor
    def __init__(self):
        """Sets up the counter."""
        Counter.instances += 1
        self.reset()

    # Mutator methods
    def reset(self):
        """Sets the counter to 0."""
        self._value = 0

    def increment(self, amount=1):
        """Adds amount to the counter."""
        self._value += amount

    def decrement(self, amount=1):
        """Subtracts amount from the counter."""
        self._value -= amount

    # Accessor methods
    def getValue(self):
        """Returns the counter's value."""
        return self._value

    def __str__(self):
        """Returns the string representation of the counter."""
        return str(self._value)

    def __eq__(self, other):
        """Returns True if self equals other

        or False otherwise."""
        if self is other: return True
        if type(self) != type(other): return False
        return self._value == other._value


def fib(n, counter):
    """统计斐波那契函数被外部调用的次数"""
    counter.increment()
    if n < 3:
        return 1
    else:
        return fib(n - 1, counter) + fib(n - 2, counter)


problemSize = 2
print("%12s%15s" % ("Problem Size", "Calls"))

for count in range(5):
    """随着问题规模增加，输出斐波那契递归函数被外部调用的次数"""
    counter = Counter()
    # 算法开始
    fib(problemSize, counter)
    # 算法结束
    print("%12d%15s" % (problemSize, counter))
    problemSize *= 2

# 运行结果：
# Problem Size          Calls
#            2              1
#            4              5
#            8             41
#           16           1973
#           32        4356617
```

### 3.1.3.衡量算法使用的内存

对于算法所用资源的分析也需要包含它所需的内存量的分析。和前面类似的问题也会存在，一些算法会随着问题规模变大而需要额外更多的内存。

### 3.1.4.练习题

1. 编写一个测试程序，这个程序统计并显示出下面这个循环的迭代次数。

   ```python
    while problemSize > 0:
        problemSize = problemSize // 2
   ```

   解答：

   ```python
   def count_iterations(problemSize):
       iterations = 0  # 初始化计数器
   
       while problemSize > 0:
           problemSize = problemSize // 2
           iterations += 1  # 每次循环迭代，计数器加一
   
       return iterations
   
   problemSize = 1000  # 设置问题规模
   iterations = count_iterations(problemSize)
   print(f"Problem Size: {problemSize}")
   print(f"Iterations: {iterations}")
   
   # 运行结果：
   # Problem Size: 1000
   # Iterations: 10
   ```

2. 在问题规模分别为1000、2000、4000、10000和100000时，运行在练习1里所创建的程序。当问题规模翻倍或是乘以10时，迭代次数会如何变化？

   解答：分别以不同的问题规模运行上面的代码，结果如下：

   ```python
   Problem Size: 1000
   Iterations: 10
   Problem Size: 4000
   Iterations: 12
   Problem Size: 8000
   Iterations: 13
   Problem Size: 10000
   Iterations: 14
   Problem Size: 100000
   Iterations: 17
   ```

3. 两次调用函数`time.time()`的结果之差就是运行时。由于操作系统也可能会在这段时间内使用CPU，因此这个运行时可能并不能反映出Python代码使用CPU的实际时间。浏览Python文档，找出另一种可以完整记录处理时间的方法，并描述如何实现它。

   解答：

   在Python中，`time` 模块提供了更精确的计时功能，其中的 `time.perf_counter()` 函数可以用来测量时间的精确间隔。与 `time.time()` 不同，`time.   perf_counter()` 会在大多数平台上提供一个更高分辨率的计时器，可以用来测量代码块的执行时间。

   `time.perf_counter()` 返回一个浮点数，表示从某个特定时间点到现在经过的秒数。以下是如何使用 `time.perf_counter()` 来计算代码块的执行时间：

   ```python
   import time
   
   # 获取起始时间（包括CPU时间和系统时间）
   start_cpu_time = time.process_time()
   start_real_time = time.perf_counter()
   start_system_time = time.time()
   
   # 执行代码
   for i in range(100000000):
       _ = i * i
   
   # 获取结束时间（包括CPU时间和系统时间）
   end_cpu_time = time.process_time()
   end_real_time = time.perf_counter()
   end_system_time = time.time()
   
   # 计算CPU时间差
   cpu_execution_time = end_cpu_time - start_cpu_time
   real_execution_time = end_real_time - start_real_time
   system_execution_time = end_system_time - start_system_time
   
   print(f"CPU Execution Time: {cpu_execution_time:.6f} seconds")
   print(f"Real Execution Time: {real_execution_time:.6f} seconds")
   print(f"System Execution Time: {system_execution_time:.6f} seconds")
   
   # 运行结果：
   # CPU Execution Time: 7.157305 seconds
   # Real Execution Time: 7.156638 seconds
   # System Execution Time: 7.156638 seconds
   ```

   在上面代码中，`start_system_time` 和 `end_system_time` 分别记录了代码块开始和结束时的系统时间。然后，可以通过计算 `end_system_time - start_system_time` 来获取系统时间的消耗。

   系统时间的计算可能受到系统的影响，可能会因为系统时间的变化而产生不准确的结果。在进行性能测试时，尽量以CPU时间和实际经过时间为主要参考指标。

   补充：

   CPU 时间、实际经过时间和系统时间代表了不同的时间指标，它们之间有以下区别：

   CPU 时间：
   - CPU 时间是程序在 CPU 上执行的时间，包括了在用户态（执行应用程序代码）和内核态（执行操作系统代码）的时间。因此，它考虑了应用程序和操作系统的执行时间。
   - CPU 时间通常用于测量程序的计算密集型工作量，即大量计算操作，比如循环和数学计算。
   - 通过 `time.process_time()` 函数可以获取当前进程的 CPU 时间。

   实际经过时间：
   - 实际经过时间是从某个时间点到现在的实际经过的时间，考虑了所有因素，包括了 CPU 时间、等待时间、系统调度等。
   - 实际经过时间用于测量代码的总执行时间，包括了计算和等待的时间。
   - 通过 `time.perf_counter()` 函数可以获取当前时间。

   系统时间：
   - 系统时间是操作系统内部维护的一个时间值，它代表了从某个固定时间点开始的秒数。
   - 系统时间通常用于记录事件和计算时间间隔，不受程序的执行影响。
   - 通过 `time.time()` 函数可以获取当前的系统时间。

   总结：CPU 时间关注的是程序在 CPU 上的执行时间，实际经过时间关注的是从代码开始到结束所经过的真实时间，系统时间是系统维护的全局时间。在不同的场景中，你可以根据需要选择合适的时间指标来进行性能测量和分析。

## 复杂度分析

## 搜索算法

## 基本的排序算法

## 更快的排序

## 指数复杂度的算法

## 案例研究

## 小结

## 复习题

## 练习题
