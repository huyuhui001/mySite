#!/usr/bin/python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Queue():
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        return self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)


if __name__ == '__main__':
    q = Queue()
    q.isEmpty()
    q.enqueue(2)
    q.enqueue('h')
    q.size()
    q.isEmpty()
    q.dequeue()
    q.size()

 
 
print("hello\r123")

