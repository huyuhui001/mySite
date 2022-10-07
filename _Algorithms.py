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


def hotPotato(namelist, num):
    simqueue = Queue()

    for name in namelist:
        simqueue.enqueue(name)
    
    while simqueue.size() > 1:
        for i in range(num):
            simqueue.enqueue(simqueue.dequeue())
        
        simqueue.dequeue()

    return simqueue.dequeue()


if __name__ == '__main__':
    hotPotato(["Bill", "David", "Susan", "Jane", "Ken", "Brad"], 7)

 
 

