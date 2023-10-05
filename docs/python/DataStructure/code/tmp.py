class Node(object):
    """单向链接节点类"""

    def __init__(self, data, next=None):
        """实例化一个节点, 默认后继节点为None"""
        self.data = data
        self.next = next


class TwoWayNode(Node):
    """双向链接节点类"""

    def __init__(self, data, previous=None, next=None):
        """实例化一个节点, 默认前序节点尾None, 默认后继节点为None"""
        Node.__init__(self, data, next)
        self.previous = previous


class LinkedList:
    """将列表元素转移为单向链接结构里的数据，并保留元素的顺序不变"""

    def __init__(self):
        """初始化head"""
        self.head = None

    def insert_from_list(self, data_list):
        """将列表元素插入单向链接结构中"""
        for data in reversed(data_list):
            self.head = Node(data, self.head)

    def search(self, target):
        """在单向链表中搜索指定元素"""
        current = self.head
        while current:
            if current.data == target:
                return True
            current = current.next
        return False
    
    def find(self, index):
        """返回单向链表中第index个元素, 假设 0 <= index < n"""
        probe = self.head
        while index > 0:
            probe = probe.next
            index -= 1
        return probe.data

    def print_list(self):
        """打印输出单向链表内容"""
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()


def main():
    print("------")
    # 创建一个单向链接结构，并打印出它的内容
    head = None
    # 在链接结构的开头依次插入五个节点
    for count in range(1, 6):
        head = Node(count, head)
    # 打印输出这个单向链接的五个节点的内容
    probe = head
    while probe != None:
        print(probe.data)
        probe = probe.next

    # 将列表中的元素插入到链接结构实例中，再使用print_list方法打印出链表中所有元素。
    print("------")
    data_list = [1, 2, 3, 4, 5]

    linked_list = LinkedList()
    linked_list.insert_from_list(data_list)
    linked_list.print_list()  # 输出: 1 2 3 4 5
    # 搜索指定元素
    print(linked_list.search(3))  # 输出: True
    print(linked_list.search(6))  # 输出: False
    print(linked_list.find(2))  # 输出：3（链表第3个元素）


if __name__ == "__main__":
    main()

# 运行结果
# ------
# 5
# 4
# 3
# 2
# 1
# ------
# 1 2 3 4 5 
# True
# False
# 3
