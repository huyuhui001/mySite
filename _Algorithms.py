#!/usr/bin/python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Stack():
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[len(self.items) - 1]
    
    def size(self):
        return len(self.items)


def matches(open, close):
    opens = "([{"
    closers = ")]}"

    return opens.index(open) == closers.index(close)


def parChecker(symbolString):
    s = Stack()

    matched = True
    index = 0

    while index < len(symbolString) and matched:
        symbol = symbolString[index]

        if symbol in "([{":
            s.push(symbol)
        else:
            if s.isEmpty():
                matched = False
            else:
                top = s.pop()
                if not matches(top, symbol):
                    matched = False
        
        index = index + 1

    if matched and s.isEmpty():
        return True, f"{symbolString}"
    else:
        return False


if __name__ == '__main__':
    parChecker("([[{}])")
    parChecker("([{}])")

