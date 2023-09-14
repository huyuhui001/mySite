import time
import random

class Profiler(object):
    """
    定义一个Profiler类, 用来分析排序算法。
    A Profiler object tracks the list, the number of comparisons and exchanges, and the running time. 
    Profiler对象跟踪一个列表的比较次数、交换次数、和运行时间。
    The Profiler can also print a trace and can create a list of unique or duplicate numbers.
    Example use:
    from profiler import Profiler
    from algorithms import selectionSort
    p = Profiler()
    p.test(selectionSort, size = 15, comp = True,
            exch = True, trace = True)
    """

    def test(self, function, lyst = None, size = 10,
             unique = True, comp = True, exch = True,
             trace = False):
        """
        function: the algorithm being profiled
        target: the search target if profiling a search
        lyst: allows the caller to use her list
        size: the size of the list, 10 by default
        unique: if True, list contains unique integers
        comp: if True, count comparisons
        exch: if True, count exchanges
        trace: if True, print the list after each exchange
        Run the function with the given attributes and print
        its profile results.
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
         """Counts exchanges if on."""
         if self.exch:
              self.exchCount += 1
         if self.trace:
              print(self.lyst)

    def comparison(self):
         """Counts comparisons if on."""
         if self.comp:
              self.cmpCount += 1

    def startClock(self):
         """Record the starting time."""
         self.start = time.time()

    def stopClock(self):
         """Stops the clock and computes the elapsed time
         in seconds, to the nearest millisecond."""
         self.elapsedTime = round(time.time() - self.start, 3)

    def __str__(self):
         """Returns the results as a string."""
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
            profiler.comparison()                # Count
            if lyst[j] < lyst[minIndex]:
                minIndex = j
            j += 1
        if minIndex != i:
            swap(lyst, minIndex, i, profiler)
        i += 1

def swap(lyst, i, j, profiler):
    """Exchanges the elements at positions i and j."""
    profiler.exchange()                                   # Count
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp

def main():
    p = Profiler()
    p.test(selectionSort) # Default behavior
    p.test(selectionSort, size = 5, trace = True)
    p.test(selectionSort, size = 100)
    p.test(selectionSort, size = 1000)
    p.test(selectionSort, size = 10000, exch = False, comp = False)

if __name__ == "__main__":
     main()

# >>> from profiler import Profiler
# >>> from algorithms import selectionSort
# >>> p = Profiler()
# >>> p.test(selectionSort)       # Default behavior
# Problem size: 10
# Elapsed time: 0.0
# Comparisons:  45
# Exchanges:    7
# >>> p.test(selectionSort, size = 5, trace = True)
# [4, 2, 3, 5, 1]
# [1, 2, 3, 5, 4]
# Problem size: 5
# Elapsed time: 0.117
# Comparisons:  10
# Exchanges:    2
# >>> p.test(selectionSort, size = 100)
# Problem size: 100
# Elapsed time: 0.044
# Comparisons:  4950
# Exchanges:    97
# >>> p.test(selectionSort, size = 1000)
# Problem size: 1000
# Elapsed time: 1.628
# Comparisons:  499500
# Exchanges:    995
# >>> p.test(selectionSort, size = 10000,
#            exch = False, comp = False)
# Problem size: 10000
# Elapsed time: 111.077