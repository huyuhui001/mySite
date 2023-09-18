import random


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
    my_array = Array(5)
    print("The array is", my_array)
    print("__len__() of the array:", my_array.__len__())
    print("len() of the arry:", len(my_array))

    for i in len(my_array):
        my_array[i] = i
        print(i)

# 运行结果：
# The array is [None, None, None, None, None]
# __len__() of the array: 5
# len() of the arry: 5

if __name__ == "__main__":
    main()

# 运行结果：
