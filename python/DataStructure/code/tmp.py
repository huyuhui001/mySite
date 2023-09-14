import time
import random


class Profiler(object):
    """
    定义一个Profiler类, 用来分析排序算法。
    Profiler对象跟踪一个列表的比较次数、交换次数、和运行时间。
    Profiler对象也能输出上述追踪信息, 并创建一个含有重复或不重复数字的列表。
    示例：
    from profiler import Profiler
    from algorithms import selectionSort
    p = Profiler()
    p.test(selectionSort, size = 15, comp = True, exch = True, trace = True)
    """

    def test(self,
             function,
             lyst=None,
             size=10,
             unique=True,
             comp=True,
             exch=True,
             trace=False):
        """
        function: 配置的算法
        target: 配置的搜索目标
        lyst: 允许调用者使用的列表
        size: 列表的大小, 默认值是10
        unique: 如果是True, 则列表包含不重复的整数
        comp: 如果是True, 则统计比较次数
        exch: 如果是True, 则统计交换次数
        trace: 如果是True, 则在每次交换后都输出列表内容

        此函数依据给定的上述属性, 打印输出相应的结果
        """
        self.comp = comp
        self.exch = exch
        self.trace = trace
        if lyst != None:
            self.lyst = lyst
        elif unique:
            self.lyst = list(range(1, size + 1))
            random.shuffle(self.lyst)
        else:
            self.lyst = []
        for count in range(size):
            self.lyst.append(random.randint(1, size))
        self.exchCount = 0
        self.cmpCount = 0
        self.startClock()
        function(self.lyst, self)
        self.stopClock()
        print(self)

    def exchange(self):
        """统计交换次数"""
        if self.exch:
            self.exchCount += 1
        if self.trace:
            print(self.lyst)

    def comparison(self):
        """统计交换次数"""
        if self.comp:
            self.cmpCount += 1

    def startClock(self):
        """记录开始时间"""
        self.start = time.time()

    def stopClock(self):
        """停止计时并以秒为单位计算消耗时间"""
        self.elapsedTime = round(time.time() - self.start, 3)

    def __str__(self):
        """以字符串方式返回结果"""
        result = "Problem size: "
        result += str(len(self.lyst)) + "\n"
        result += "Elapsed time: "
        result += str(self.elapsedTime) + "\n"
        if self.comp:
            result += "Comparisons: "
            result += str(self.cmpCount) + "\n"
        if self.exch:
            result += "Exchanges: "
            result += str(self.exchCount) + "\n"
        return result


def selectionSort(lyst, profiler):
    i = 0
    while i < len(lyst) - 1:
        minIndex = i
        j = i + 1
        while j < len(lyst):
            profiler.comparison()  # Count
            if lyst[j] < lyst[minIndex]:
                minIndex = j
            j += 1
        if minIndex != i:
            swap(lyst, minIndex, i, profiler)
        i += 1


def swap(lyst, i, j, profiler):
    """交换处于位置i和j的元素"""
    profiler.exchange()  # Count
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp


def main():
    p = Profiler()

    # 默认行为
    print("The result of p.test(selectionSort)")
    p.test(selectionSort)

    print("The result of p.test(selectionSort, size=5, trace=True)")
    p.test(selectionSort, size=5, trace=True)

    print("The result of p.test(selectionSort, size=100)")
    p.test(selectionSort, size=100)

    print("The result of p.test(selectionSort, size=1000)")
    p.test(selectionSort, size=1000)

    print(
        "The result of p.test(selectionSort, size=10000, exch=False, comp=False)"
    )
    p.test(selectionSort, size=10000, exch=False, comp=False)


if __name__ == "__main__":
    main()

# 运行结果：
# The result of p.test(selectionSort)
# Problem size: 20
# Elapsed time: 0.0
# Comparisons: 190
# Exchanges: 12

# The result of p.test(selectionSort, size=5, trace=True)
# [5, 1, 4, 3, 2, 1, 1, 2, 4, 4]
# [1, 5, 4, 3, 2, 1, 1, 2, 4, 4]
# [1, 1, 4, 3, 2, 5, 1, 2, 4, 4]
# [1, 1, 1, 3, 2, 5, 4, 2, 4, 4]
# [1, 1, 1, 2, 3, 5, 4, 2, 4, 4]
# [1, 1, 1, 2, 2, 5, 4, 3, 4, 4]
# [1, 1, 1, 2, 2, 3, 4, 5, 4, 4]
# [1, 1, 1, 2, 2, 3, 4, 4, 5, 4]
# Problem size: 10
# Elapsed time: 0.0
# Comparisons: 45
# Exchanges: 8

# The result of p.test(selectionSort, size=100)
# Problem size: 200
# Elapsed time: 0.003
# Comparisons: 19900
# Exchanges: 195

# The result of p.test(selectionSort, size=1000)
# Problem size: 2000
# Elapsed time: 0.36
# Comparisons: 1999000
# Exchanges: 1992

# The result of p.test(selectionSort, size=10000, exch=False, comp=False)
# Problem size: 20000
# Elapsed time: 26.535
