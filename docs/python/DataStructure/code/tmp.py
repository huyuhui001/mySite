def sequentialSearch(target, lyst):
    """找到目标元素时返回元素的索引, 否则返回-1"""
    position = 0
    while position < len(lyst):
        if target == lyst[position]:
            return position
        position += 1
    return -1


def main():
    myList = [2, 20, 5, 0, 1, 0, 9]
    locatedIndex = sequentialSearch(9, myList)
    print(locatedIndex, myList[locatedIndex])


if __name__ == "__main__":
    main()

# 运算结果：
# 6 9