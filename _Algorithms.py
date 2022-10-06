#!/usr/bin/python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Stack():
    def __init__(self) -> None:
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        self.items.pop()
    
    def peek(self):
        return self.items[len(self.items) - 1]
    
    def size(self):
        return len(self.items)

s = Stack()
s.isEmpty()
s.push(4)
s.push('dog')
s.peek()
s.size()
s.isEmpty()
s.push(6.6)
s.pop()
s.size()




