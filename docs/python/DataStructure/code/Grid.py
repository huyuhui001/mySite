class Array(object):
    """描述一个数组。"""

    def __init__(self, capacity, fillValue=None):
        """Capacity是数组的大小.  fillValue会填充在每个元素位置, 默认值是None"""
        # 初始化数组的逻辑尺寸和物理尺寸
        self.logicalSize = 0
        self.capacity = capacity
        self.fillValue = fillValue
        #初始化内部数组，并填充元素值
        self.items = list()
        for count in range(capacity):
            self.items.append(fillValue)
            self.logicalSize += 1  # 初始化数组物理大小时，也同时初始化其逻辑大小

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
            raise IndexError("读取操作出错, 数组索引越界(不在数组逻辑边界范围内)")

        return self.items[index]

    def __setitem__(self, index, newItem):
        """
        下标运算符用于在索引处进行替换.
        先决条件: 0 <= index < size()
        """
        if index < 0 or index >= self.size():
            raise IndexError("更新操作出错, 数组索引越界(不在数组逻辑边界范围内)")
        self.items[index] = newItem

    def __eq__(self, other):
        """
        两个数组相等则返回True, 否则返回False
        """
        # 判断两个数组是否是同一个对象，注意，不是它们的值是否相等
        if self is other:
            return True
        # 判断两个对象类型是否一样
        if type(self) != type(other):
            return False
        # 判断两个数组大小是否一样
        if self.size() != other.size():
            return False
        # 比较两个数组的值是否一样
        for index in range(self.size()):
            if self[index] != other[index]:
                return False
        return True

    def grow(self):
        """增大数组物理尺寸"""
        # 基于当前物理尺寸加倍，并将fillValue赋值底层列表的新元素
        for count in range(len(self)):
            self.items.append(self.fillValue)

    def insert(self, index, newItem):
        """在数组指定索引处插入新元素"""
        # 当数组的物理尺寸和逻辑尺寸一样时，则增加物理尺寸
        if self.size() == len(self):
            self.grow()
        # 插入新元素
        # 当插入位置大于或等于最大逻辑位置，则在数组末端插入新元素
        # 当插入位置介于数组逻辑位置的中间，则从插入位置起将剩余数组元素向尾部平移一个位置
        if index >= self.size():
            self.items[self.size()] = newItem
        else:
            index = max(index, 0)

            # 将数组元素向尾部平移一个位置
            for i in range(self.size(), index, -1):
                self.items[i] = self.items[i - 1]

            # 插入新元素
            self.items[index] = newItem

        # 增加数组的逻辑尺寸
        self.logicalSize += 1

    def shrink(self):
        """
        减少数组的物理尺寸
        当:
        - 数组的逻辑尺寸小于或等于其物理尺寸的1/4
        - 并且它的物理尺寸至少是这个数组建立时默认容量的2倍时
        则把数组的物理尺寸减小到原来的一半，并且也不会小于其默认容量
        """
        # 在逻辑尺寸和物理尺寸的一半之间选择最大值作为数组收缩后的物理尺寸
        newSize = max(self.capacity, len(self) // 2)
        # 释放多余的数组空间
        for count in range(len(self) - newSize):
            self.items.pop()

    def pop(self, index):
        """
        删除指定索引值的数组元素,并返回删除的数组元素值
        先决条件: 0 <= index < size()
        """
        if index < 0 or index >= self.size():
            raise IndexError("删除操作出错, 数组索引越界(不在数组逻辑边界范围内)")

        # 保存即将被删除的数组元素值
        itemToReturn = self.items[index]

        # 将数组元素向头部平移一个位置
        for i in range(index, self.size() - 1):
            self.items[i] = self.items[i + 1]

        # 将数组尾部的空余位赋值fillValue，默认是None
        self.items[self.size() - 1] = self.fillValue

        # 减少数组逻辑尺寸
        self.logicalSize -= 1

        # 减少数组物理尺寸
        # 当:
        # - 数组的逻辑尺寸小于或等于其物理尺寸的1/4
        # - 并且它的物理尺寸至少是这个数组建立时默认容量的2倍时
        # 则把数组的物理尺寸减小到原来的一半，并且也不会小于其默认容量
        if self.size() <= len(self) // 4 and len(self) > self.capacity:
            self.shrink()

        # 返回被删除元素的值
        print(f'Item {itemToReturn} was deleted')
        return itemToReturn


class Grid(object):
    """描述一个二维数组。"""

    def __init__(self, rows, columns, fillValue=None):
        self.rows = rows
        self.columns = columns
        self.fillValue = fillValue
        # 按行数初始化数组y轴物理尺寸
        self.data = Array(rows, fillValue)
        # 按列数初始化数组x轴物理尺寸，并赋值到y轴数组，填充None值
        for row in range(rows):
            self.data[row] = Array(columns, fillValue)

    def getHeight(self):
        """返回二维数组的y轴的大小(物理尺寸), 即数组的行数"""
        return len(self.data)

    def getWidth(self):
        """返回二维数组的x轴的大小(物理尺寸), 即数组的列数"""
        return len(self.data[0])

    def __getitem__(self, index):
        """返回二维数组指定行和列索引对应的元素值"""
        return self.data[index]

    def __str__(self):
        """返回二维数组的字符串形式"""
        result = ""
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                result += str(self.data[row][col]) + " "
            result += "\n"
        return result


def main():
    my_grid = Grid(5, 5, 1)
    print(my_grid)


if __name__ == "__main__":
    main()

# 运行结果
# 1 1 1 1 1 
# 1 1 1 1 1 
# 1 1 1 1 1 
# 1 1 1 1 1 
# 1 1 1 1 1 