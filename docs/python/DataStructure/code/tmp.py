# class Node(object):
#     """单向链接节点类"""

#     def __init__(self, data, next=None):
#         """实例化一个节点, 默认后继节点为None"""
#         self.data = data
#         self.next = next

# class TwoWayNode(Node):
#     """双向链接节点类"""

#     def __init__(self, data, previous=None, next=None):
#         """实例化一个节点, 默认前序节点尾None, 默认后继节点为None"""
#         Node.__init__(self, data, next)
#         self.previous = previous

# class LinkedList:
#     """单向和双向链接结构"""

#     def __init__(self, node):
#         # 初始化头节点
#         self.head = node
#         # 属性size保存链接结构的逻辑大小，通常指的是链表所包含的元素的数量，初始化链接结构大小为0
#         self.size = 0

#     def insert_from_list(self, data_list, twoway=False):
#         """
#         把一个列表（已有的数据结构）转换为链接结构是一种比较常见实用的方式。这种做法可以通过控制代码，方便地从已有的集合类（如列表，数组等）中导入元素，并构建需要的的链接结构。
#         在一些简单场景下，比如已知待添加的元素数量很少，或者有其他约束使得用列表不方便时，可以通过手动方式向链接结构添加元素。但如果元素很多，或者有未知数量的元素需要添加，用列表可以方便地一次性导入所有元素。
#         """
#         if twoway:  # 检查是否要创建双向链表
#             for data in data_list:  # 对于数据列表中的每个数据创建一个新的双向链接节点
#                 node = TwoWayNode(data)

#                 if self.head is None:  # 如果链表为空把新节点设置为头节点
#                     self.head = node
#                 else:  # 如果链表不为空
#                     tail = self.head  # 从头节点开始
#                     while tail.next is not None:  # 通过遍历链表查找尾节点
#                         tail = tail.next
#                     tail.next = node  # 把新节点插入到尾节点
#                     node.previous = tail  # 设置新节点的前一个节点指向尾节点
#         else:  # 创建单向链表
#             for data in reversed(data_list):  # 对于列表中的每个元素，反向迭代使得插入的节点与原数据顺序相同
#                 self.head = Node(data, self.head)  # 创建一个新的单向链接节点并插入到头节点
#         self.size += len(data_list)  # 更新链表大小

#     def get_size(self):
#         """获取链表大小（节点数量）"""
#         return self.size

#     def search(self, target):
#         """在链接结构中搜索指定元素"""
#         current = self.head  # 从头节点开始
#         while current:  # 当当前节点非None时继续遍历
#             if current.data == target:  # 如果当前节点的数据等于目标数据
#                 return True  # 返回真值
#             current = current.next  # 移动到下一节点
#         return False  # 如果整个链表遍历完毕还找不到目标数据，返回假值

#     def locate(self, index):
#         """返回链接结构中第index个元素, 0 <= index < n"""
#         if index >= self.get_size() or index < 0:   # 如果索引超出范围，立即抛出错误
#             raise IndexError("链表索引超出范围")

#         probe = self.head  # 确定起始点为头节点
#         while index > 0:  # 当索引大于0时，进入循环
#             probe = probe.next  # 将探针（probe）移动到下一个节点
#             index -= 1  # 将索引值减1
#         return probe.data  # 返回当前位置（index对应位置）的节点数据

#     def replace(self, old, new):
#         """替换链表中所有等于old的元素为new"""
#         current = self.head  # 从链表的头节点开始遍历
#         while current:  # 只要还有节点，就继续遍历
#             if current.data == old:  # 检查当前节点的数据是否等于old
#                 current.data = new  # 如果等于old，将当前节点的数据替换为new
#             current = current.next  # 继续检查下一个节点

#     def print_list(self):
#         """打印输出链接结构内容"""
#         current = self.head
#         while current:
#             print(current.data, end=' ')
#             current = current.next
#         print()

# def main():
#     # 创建测试数据
#     test_data = [1, 2, 3, 4, 5]

#     # 单向链表测试
#     print("单向链表测试:")
#     single_linked_list = LinkedList(None)
#     print("插入数据")
#     single_linked_list.insert_from_list(test_data)  # 插入测试数据
#     single_linked_list.print_list()  # 打印链接结构内容
#     print("链表大小：", single_linked_list.get_size())  # 显示链接结构大小
#     print("搜索元素3: ", single_linked_list.search(3))  # 搜索链接结构中是否存在元素3
#     print("查找第2个元素: ", single_linked_list.locate(2))  # 查找链接结构中第2个元素
#     print("把元素1替换为10")
#     single_linked_list.replace(1, 10)  # 替换元素1为10
#     single_linked_list.print_list()

#     print()

#     # 双向链表测试
#     print("双向链表测试:")
#     double_linked_list = LinkedList(None)
#     print("插入数据")
#     double_linked_list.insert_from_list(test_data, twoway=True)
#     double_linked_list.print_list()
#     print("链表大小：", double_linked_list.get_size())
#     print("搜索元素3：", double_linked_list.search(3))
#     print("查找第2个元素：", double_linked_list.locate(2))
#     print("替换元素1为10")
#     double_linked_list.replace(1, 10)
#     double_linked_list.print_list()

# if __name__ == "__main__":
#     main()

# # 运行结果
# # 单向链表测试:
# # 插入数据
# # 1 2 3 4 5
# # 链表大小： 5
# # 搜索元素3： True
# # 查找第2个元素： 3
# # 替换元素1为10
# # 10 2 3 4 5

# # 双向链表测试:
# # 插入数据
# # 1 2 3 4 5
# # 链表大小： 5
# # 搜索元素3： True
# # 查找第2个元素： 3
# # 替换元素1为10
# # 10 2 3 4 5


class Node(object):
    """单向链接节点类"""

    def __init__(self, data, next=None):
        """实例化一个节点, 默认后继节点为None"""
        self.data = data
        self.next = next


def main():
    head = None  # 创建一个空链表
    for count in range(1, 6):  # 从1到5遍历
        newNode = Node(count)
        if head is None:
            head = newNode
        else:
            probe = head
            while probe.next != None:
                probe = probe.next
            probe.next = newNode

    while head != None:  # 从头节点开始遍历链表
        print(head.data)  # 打印当前节点的数据
        head = head.next  # 移动到下一个节点


if __name__ == "__main__":
    main()
