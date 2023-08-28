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

## 3.1.衡量算法的效率

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

下面的算法中，迭代次数和问题规模的平方。这就解释了为什么这个算法的耗时非常大。

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

## 3.2.复杂度分析

复杂度分析（complexity analysis）方法，一种评估算法效率的方法，这个方法可以不用关心与平台相关的时间，也不需要使用统计指令数量这种方法来对算法进行评估。

### 3.2.1.复杂度的阶

在`3.1.2.统计指令数`中关于迭代次数和问题规模的两个算法，它们复杂度的阶（order of complexity）上是不一样的。

- 第一个算法中，迭代次数和问题规模之间是线性关系，称其复杂度为线性（linear）阶；
- 第二个算法中，迭代次数和问题规模之间是平方关系，称其复杂度为平方（quadratic）阶；

如果算法需要相同数量的运算，那么它的性能就是常数（constant）阶。列表索引就是一个常数时间算法的例子。

比线性性能好，但比常数性能差的另一个复杂度的阶被称为对数（logarithmic）阶。对数算法的工作量与问题规模的以2为底的对数成正比。当问题规模扩大一倍时，工作量只会加1。

多项式时间算法（polynomial time algorithm）的工作量会以`n^k`的速率增长，其中`k`是大于`1`的常数，比如`n^2`、`n^3`以及`n^10`。从某种意义上讲，`n^3`的性能要比`n^2`差，但都属于多项式（polynomial）阶。

比多项式还要差的复杂度的阶被称为指数（exponential）阶，比如`2^n`。对于大的问题规模来说，指数算法是不可行的。

不同复杂度阶的算法的工作量比较（从小到大）：对数阶 < 线性阶 < 平方阶 < 指数阶。随着问题规模的增大，具有较高复杂度的阶的算法的性能会更快地变差。

### 3.2.2.大O表示法

很多情况下，算法中的工作量通常是多项式里多项的总和，而当工作量表示为多项式时，其中一项是主导项（dominant）。随着`n`越来越大，主导项将变得非常大，以至于可以忽略其他项所代表的工作量。因此，对于多项式`n^2+n`，只需要着重考虑平方项`n^2`，也就是在考虑的时候可以忽略线性项`n`。随着`n^2`变得非常大，多项式的值渐近地接近或近似于它的最大项值，这种形式的分析有时被称为渐近分析（asymptotic analysis）。

计算中用来表示算法的效率或计算复杂度的一种方法被称为大O表示法（big-O notation）。“O”代表“在……阶”，指的是算法工作的复杂度的阶。例如：

- 常数时间：O(1)
- 线性时间：O(n)
- 平方时间：O(n^2)
- 立方时间：O(n^3)
- 多项式时间：O(n^k)

### 3.2.3.比例常数的作用

比例常数（constant of proportionality）包含在大O分析中被忽略的项和系数。比如，线性时间算法所执行的工作量可以表示为：`work = 2 * size`，其中比例常数就是`work/size`，也就是`2`。在处理中小型数据集的时候，如果这些常数很大，那么它们也会影响到算法效率。

回顾下面的例子。

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

其中的算法部分，除了循环语句本身，还有其他3行代码，它们都是复制语句，都会以常数时间运行。假设循环语句本身会消耗一个时间常数，那么这个算法的抽象工作时间就是`3n+1`。虽然`3n+1`的工作量大于`n`，但二者在运行时都是线性增加，所以他们运行时都是`O(n)`。

```python
    # 算法开始
    work = 1
    for x in range(problemSize):
        number += 1
        work += 1
        work -= 1
    # 算法结束
```

### 3.2.4.练习题

1. 假设下面的表达式都分别表示对问题规模为`n`的算法所需要执行的操作数，请指出每种算法中的主导项，并使用大O表示法对它进行分类。
   a. 2^n - 4n + 5n
   b. 2n^2 + 8
   c. n^3  n^2 + n

   解答：
   a. 2^n，O(n)
   b. n^2，O(n^2)
   c. n^3，O(n^3)

2. 对于规模为`n`的问题，算法A和B分别会执行`n^2`和`(1/2)*n^2+(1/2)*n`条指令。哪种算法更高效？有没有一种算法比另一种算法性能明显更好的特定的问题规模？是否有让两种算法都执行大致相同工作量的特定的问题规模？

   解答：

   在比较两种算法的效率时，通常关注算法执行时间随问题规模增长的趋势。题目中的两种算法的执行指令数分别如下：

   - 算法A：执行 `n^2` 条指令。
   - 算法B：执行 `(1/2)*n^2+(1/2)*n` 条指令。

   用如下代码模拟算法A和算法B，可以看出，随着`n`的增加，算法A的增长速率远大于算法B。所以可以认为在`n >= 2`的情况下，算法A优于算法B。

   ```python
   n = 1
   print("%-15s%25s" % ("ProblemSize: n", "A/B"))
   while n < 1000000:
       n *= 10
       print("%-15d%25d" % (n, int((n**2) / (1 / 2) * n**2 + (1 / 2) * n)))
   
   # ProblemSize: n                       A/B
   # 10                                 20005
   # 100                            200000050
   # 1000                       2000000000500
   # 10000                  20000000000005000
   # 100000             200000000000000065536
   # 1000000        1999999999999999966445568
   ```

   由此可得，在大问题规模下，算法B的增长速率会更慢，因为`(1/2)*n^2+(1/2)*n`中的`(1/2)*n`部分对于整体增长来说相对较小。

   为了让两种算法执行相近的工作量，我们可以解下面的方程：

   ```python
   (1/2)*n^2+(1/2)*n = k * n^2
   ```

   其中`k`是一个常数，表示两种算法执行的工作量相等时的问题规模。通过解这个方程，我们可以找到一个问题规模 `k`，在这个问题规模下，两种算法的执行指令数相近。

   算法的效率分析并不仅仅取决于指令数，还可能受到算法中常数因子、数据访问模式、内存占用等因素的影响。因此，在实际应用中，通常需要综合考虑多个因素来确定最优的算法选择。

3. 在什么时候开始`n^4`算法比`2^n`算法表现更好？

   解答：用下面的算法模拟`n^4`算法比`2^n`算法执行工作量。从运行结果可以看出：

   - `n=16`是分界点，`n^4`算法与`2^n`算法工作量相等；
   - 当`n<16`时，`n^4`算法比`2^n`算法工作量要高；
   - 当`n>16`时，`n^4`算法比`2^n`算法工作量要低；而且`2^n`算法工作量增长速度远大于`n^4`算法；

   ```python
   n = 1
   print("%-8s%10s%15s%10s" % ("Size:n", "A:n^4", "B:2^n", "B/A"))
   while n < 30:
       n += 1
       print("%-8d%10d%15d%10.3f" % (n, int(n**4), int(2**n), (2**n) / (n**4)))
   
   # 运行结果：
   # Size:n       A:n^4          B:2^n       B/A
   # 2               16              4     0.250
   # 3               81              8     0.099
   # 4              256             16     0.062
   # 5              625             32     0.051
   # 6             1296             64     0.049
   # 7             2401            128     0.053
   # 8             4096            256     0.062
   # 9             6561            512     0.078
   # 10           10000           1024     0.102
   # 11           14641           2048     0.140
   # 12           20736           4096     0.198
   # 13           28561           8192     0.287
   # 14           38416          16384     0.426
   # 15           50625          32768     0.647
   # 16           65536          65536     1.000
   # 17           83521         131072     1.569
   # 18          104976         262144     2.497
   # 19          130321         524288     4.023
   # 20          160000        1048576     6.554
   # 21          194481        2097152    10.783
   # 22          234256        4194304    17.905
   # 23          279841        8388608    29.976
   # 24          331776       16777216    50.568
   # 25          390625       33554432    85.899
   # 26          456976       67108864   146.854
   # 27          531441      134217728   252.554
   # 28          614656      268435456   436.725
   # 29          707281      536870912   759.063
   # 30          810000     1073741824  1325.607
   ```

## 3.3.搜索算法

约定：

- 以列表为例，介绍搜索和排序的算法；
- 阐释这些算法的设计，并把它实现为Python函数；
- 函数只处理全部是整数的列表，不同大小的列表将作为参数传递给函数；
- 对这些算法的计算复杂度进行分析；

### 3.3.1.最小值搜索

Python中有`min`函数，会返回列表里的最小值或最小元素，下面写一个新算法，来分析`min`函数的算法复杂度。

算法目标：假定列表不为空，并且元素是按照任意顺序存放在列表里的，算法返回最小元素的索引（index）。

算法解析：

- 首先把第一个位置作为存放最小元素的位置；
- 然后向右侧搜索更小的元素；
- 如果找到，那么把最小元素的位置重置为当前位置；
- 当算法到达列表末尾时，它将返回最小元素的位置。

如下所示为函数indexOfMin里实现这个算法的代码。

### 3.3.2.顺序搜索列表

### 3.3.3.最好情况、最坏情况以及平均情况下的性能

### 3.3.4.基于有序列表的二分搜索

### 3.3.5.比较数据元素

### 3.3.6.练习题

## 3.4.基本的排序算法

## 3.5.更快的排序

## 3.6.指数复杂度的算法

## 3.7.案例研究:算法分析器

## 3.8.小结

## 3.9.复习题

## 3.10.练习题
