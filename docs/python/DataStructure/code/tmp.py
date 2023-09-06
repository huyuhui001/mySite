class Array(object):
    """
    描述一个数组。
    数组类似列表，但数组只能使用[], len, iter, 和 str这些属性。
    实例化一个数组，使用 <variable> = Array(<capacity>, <optional fill value>) 其中fill value默认值是None。
    """

    def __init__(self, capacity, fillValue=None):
        """Capacity是数组的大小.  fillValue会填充在每个元素位置, 默认值是None"""
        self.items = list()
        for count in range(capacity):
            self.items.append(fillValue)

    def __len__(self):
        """-> 数组的大小"""
        return len(self.items)

    def __str__(self):
        """-> 将数组字符串化"""
        return str(self.items)

    def __iter__(self):
        """支持for循环对数组进行遍历."""
        return iter(self.items)

    def __getitem__(self, index):
        """用于访问索引处的下标运算符."""
        return self.items[index]

    def __setitem__(self, index, newItem):
        """下标运算符用于在索引处进行替换."""
        self.items[index] = newItem


def mergeSort(lyst):
    # lyst       : 用于排序的列表
    # copyBuffer : 用于合并的临时空间
    copyBuffer = Array(len(lyst))
    mergeSortHelper(lyst, copyBuffer, 0, len(lyst) - 1)


def mergeSortHelper(lyst, copyBuffer, low, high):
    # lyst       : 用于排序的列表
    # copyBuffer : 用于合并的临时空间
    # low, high  : 子列表的边界
    # middle     : 子列表的中点
    if low < high:
        middle = (low + high) // 2
        print(f'low: {lyst[low]}, middle: {lyst[middle]}, high: {lyst[high]}, copyBuffer: {copyBuffer}')
        mergeSortHelper(lyst, copyBuffer, low, middle)  # 第一个排序子列表
        mergeSortHelper(lyst, copyBuffer, middle + 1, high)  # 第二个排序子列表
        merge(lyst, copyBuffer, low, middle, high)  # 合并


def merge(lyst, copyBuffer, low, middle, high):
    # lyst       : 用于排序的列表
    # copyBuffer : 用于合并的临时空间
    # low        : 第一个排序子列表的开头
    # middle     : 第一个排序子列表的结尾
    # middle + 1 : 第二个排序子列表的开头
    # high       : 第二个排序子列表的结尾
    # 将 i1 和 i2 初始化为每个子列表中的第一项
    i1 = low
    i2 = middle + 1
    # 将子列表中的元素交错放入copyBuffer中，并保持顺序。
    for i in range(low, high + 1):
        if i1 > middle:
            copyBuffer[i] = lyst[i2]  # 第一个子列表已用完
            i2 += 1
        elif i2 > high:
            copyBuffer[i] = lyst[i1]  # 第二个子列表已用完
            i1 += 1
        elif lyst[i1] < lyst[i2]:
            copyBuffer[i] = lyst[i1]  # 第一个子表中的元素 <
            i1 += 1
        else:
            copyBuffer[i] = lyst[i2]  # 第二个子表中的元素 <
            i2 += 1

    print("i=", i, "", "i1=", i1, "i2=", i2, "copyBuffer:", copyBuffer)

    for i in range(low, high + 1):  # 将已排序的元素复制回lyst中的正确位置
        lyst[i] = copyBuffer[i]


def main():
    lyst = [12, 19, 17, 18, 14, 11, 15, 13, 16]
    print("Original List", lyst)
    mergeSort(lyst)
    print("Sorted List", lyst)


if __name__ == "__main__":
    main()

# 运行结果：
# Original List [12, 19, 17, 18, 14, 11, 15, 13, 16]
# low: 12, middle: 14, high: 16, copyBuffer: [None, None, None, None, None, None, None, None, None]
# low: 12, middle: 17, high: 14, copyBuffer: [None, None, None, None, None, None, None, None, None]
# low: 12, middle: 19, high: 17, copyBuffer: [None, None, None, None, None, None, None, None, None]
# low: 12, middle: 12, high: 19, copyBuffer: [None, None, None, None, None, None, None, None, None]
# i= 1  i1= 1 i2= 2 copyBuffer: [12, 19, None, None, None, None, None, None, None]
# i= 2  i1= 2 i2= 3 copyBuffer: [12, 17, 19, None, None, None, None, None, None]
# low: 18, middle: 18, high: 14, copyBuffer: [12, 17, 19, None, None, None, None, None, None]
# i= 4  i1= 4 i2= 5 copyBuffer: [12, 17, 19, 14, 18, None, None, None, None]
# i= 4  i1= 3 i2= 5 copyBuffer: [12, 14, 17, 18, 19, None, None, None, None]
# low: 11, middle: 15, high: 16, copyBuffer: [12, 14, 17, 18, 19, None, None, None, None]
# low: 11, middle: 11, high: 15, copyBuffer: [12, 14, 17, 18, 19, None, None, None, None]
# i= 6  i1= 6 i2= 7 copyBuffer: [12, 14, 17, 18, 19, 11, 15, None, None]
# low: 13, middle: 13, high: 16, copyBuffer: [12, 14, 17, 18, 19, 11, 15, None, None]
# i= 8  i1= 8 i2= 9 copyBuffer: [12, 14, 17, 18, 19, 11, 15, 13, 16]
# i= 8  i1= 7 i2= 9 copyBuffer: [12, 14, 17, 18, 19, 11, 13, 15, 16]
# i= 8  i1= 5 i2= 9 copyBuffer: [11, 12, 13, 14, 15, 16, 17, 18, 19]
# Sorted List [11, 12, 13, 14, 15, 16, 17, 18, 19]