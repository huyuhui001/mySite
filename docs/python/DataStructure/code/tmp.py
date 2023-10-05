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

def main():
    # 创建一个空链
    node1 = None

    # 创建一个单向链接节点，含数据元素和空链
    node2 = Node("A", None)

    # 创建一个单向链接节点，含数据元素和指向下一个节点的链接
    node3 = Node("B", node2)


if __name__ == "__main__":
    main()
