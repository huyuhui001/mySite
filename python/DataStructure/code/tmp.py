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


def main(size=10):
    DEFAULT_CAPACITY = 5
    logicalSize = 0
    my_array = Array(DEFAULT_CAPACITY)

    print("Initial array is: ", my_array)
    print("Len of the array: ", my_array.__len__())

    for i in range(len(my_array)):
        my_array[i] = i

    print("The array is: ", my_array.items)

    # 增大数组物理尺寸
    if logicalSize == len(my_array):
        temp = Array(len(my_array) * 2)  # 创建一个新数组
        for i in range(logicalSize):
            temp[i] = my_array[i]  # 从原数组复制内容到新数组
        my_array = temp  # 把新数组赋值给原数组


if __name__ == "__main__":
    main()

# 运行结果：
# Initial array is:  [None, None, None, None, None]
# Len of the array:  5
# The array is:  [0, 1, 2, 3, 4]
