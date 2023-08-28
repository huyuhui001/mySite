def indexOfMin(lyst):
    """返回最小元素的索引"""

    minIndex = 0
    currentIndex = 1

    while currentIndex < len(lyst):
        if lyst[currentIndex] < lyst[minIndex]:
            minIndex = currentIndex
        currentIndex += 1
    return minIndex


def main():
    myList = [2, 20, 5, 0 , 1, 0, 9]
    minIndex = indexOfMin(myList)
    print(minIndex, myList[minIndex])

if __name__ == "__main__":
    main()

# 运算结果：
# 3 0