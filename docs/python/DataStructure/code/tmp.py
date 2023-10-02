class Array(object):
    """描述一个数组。"""

    def __init__(self, capacity, fillValue=None):
        """Capacity是数组的大小.  fillValue会填充在每个元素位置, 默认值是None"""
        # 初始化数组的逻辑尺寸和物理尺寸
        self.logicalSize = 0
        self.capacity = capacity
        #初始化内部数组，并填充元素值
        self.items = list()
        for count in range(capacity):
            self.items.append(fillValue)

    def __len__(self):
        """返回数组的大小"""
        return len(self.items)

    def __str__(self):
        """将数组字符串化并返回"""
        result = ""
        for index in range(self.size()):
            result += str(self.items[index]) + " "
        return result

    def size(self):
        """返回数组的逻辑尺寸"""
        return self.logicalSize

    def __iter__(self):
        """支持for循环对数组进行遍历."""
        print("__iter__ called")  # 仅用来测试何时__iter__会被调用
        return iter(self.items)

    def __getitem__(self, index):
        """
        用于访问索引处的下标运算符.
        先决条件: 0 <= index < size()
        """
        if index < 0 or index >= self.size():
            raise IndexError("数组索引越界(不在数组逻辑边界范围内)")
        return self.items[index]

    def __setitem__(self, index, newItem):
        """
        下标运算符用于在索引处进行替换.
        先决条件: 0 <= index < size()
        """
        if index < 0 or index >= self.size():
            raise IndexError("数组索引越界(不在数组逻辑边界范围内)")
        self.items[index] = newItem

    def grow(self):
        """Increases the physical size of the array if necessary."""
        # Double the physical size if no more room for items
        # and add the fillValue to the new cells in the underlying list
        for count in range(len(self)):
            self.items.append(self.fillValue)

def main():
    my_arr = Array(5)
    print("Physical size:", len(my_arr))
    print("Logical size:", my_arr.size())
    print("Initial items:", my_arr.items)

    # for item in range(4):
    #     my_arr.insert(0, item)
    # print ("Items:", my_arr)
    # my_arr.insert(1, 77)
    # print ("Items:", my_arr)
    # my_arr.insert(10, 10)
    # print ("Items:", my_arr)
    # print(my_arr.pop(3))
    # print ("Items:", my_arr)
    # for count in range(6):
    #     print(my_arr.pop(0), end = " ")
    # print (my_arr.pop(0))


if __name__ == "__main__":
    main()

# 运行结果
# Physical size: 5
# Logical size: 0
# Initial items: [None, None, None, None, None]

# def main(size=10):
#     # 初始值
#     DEFAULT_CAPACITY = 5
#     logicalSize = 0
#     my_array = Array(DEFAULT_CAPACITY)

#     # 打印输出初始数组信息
#     print("Initial array is: ", my_array)
#     print("Len of the array: ", my_array.__len__())

#     # 给数组赋值
#     for i in range(len(my_array)):
#         my_array[i] = i

#     print("The array is: ", my_array.items)  # 打印输出数组

#     # 增大数组物理尺寸
#     while logicalSize < DEFAULT_CAPACITY * 2:
#         logicalSize += 1
#         if logicalSize == len(my_array):  # 触发条件
#             temp = Array(len(my_array) + 1)  # 创建一个新数组
#             for i in range(logicalSize):
#                 temp[i] = my_array[i]  # 从原数组复制内容到新数组
#             my_array = temp  # 把新数组赋值给原数组

#     print("The array after increased is: ", my_array.items)  # 打印输出数组

#     # 减小数组物理尺寸
#     while logicalSize > len(my_array) // 4:
#         logicalSize -= 1
#         if logicalSize <= len(my_array) // 4 and len(my_array) >= DEFAULT_CAPACITY * 2:  # 触发条件
#             temp = Array(len(my_array) // 2)  # 创建一个新数组
#             for i in range(logicalSize):
#                 temp[i] = my_array[i]  # 从原数组复制内容到新数组
#             my_array = temp  # 把新数组赋值给原数组

#     print("The array after decreased is: ", my_array.items)  # 打印输出数组

#     # 增大数组物理尺寸，并向后移动一个索引位
#     targetIndex = 0 # 插入元素的索引位，初始值是0，在数组首部插入
#     newItem = 99 # 插入元素的值，初始值为99
#     print(logicalSize)
#     for i in range(logicalSize, targetIndex, -1):
#         my_array[i] = my_array[i - 1]
#     # Add new item and increment logical size
#     my_array[targetIndex] = newItem  # 增加一个元素
#     logicalSize += 1  # 增加数组的逻辑大小

# if __name__ == "__main__":
#     main()

# # 运行结果：
# # Initial array is:  [None, None, None, None, None]
# # Len of the array:  5
# # The array is:  [0, 1, 2, 3, 4]
# # The array after increased is:  [0, 1, 2, 3, 4, None, None, None, None, None, None]
# # The array after decreased is:  [0, 1, None, None, None]
