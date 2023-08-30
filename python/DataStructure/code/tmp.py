def binarySearch(target, sortedLyst):
    left = 0
    right = len(sortedLyst) - 1

    print("%5s%10s%10s" % ("left", "midpoint", "right"))

    while left <= right:
        midpoint = (left + right) // 2

        print("%5s%10s%10s" % (left, midpoint, right))

        if target == sortedLyst[midpoint]:
            return midpoint
        elif target < sortedLyst[midpoint]:
            right = midpoint - 1
        else:
            left = midpoint + 1

    return -1


def dictSearch(target, sortedLyst):
    left = 0
    right = len(sortedLyst) - 1

    print("%5s%10s%10s" % ("left", "midpoint", "right"))

    while left <= right:
        midpoint = (left + right) // 2
        current_name = sortedLyst[midpoint]

        print("%5s%10s%10s" % (left, midpoint, right))

        # 按首字母移动
        if current_name[0] == target[0]:  # 比较名字的首字母
            # 比较名字后续字母
            if current_name == target:
                return midpoint
            elif current_name < target:
                left = midpoint + 1
            else:
                right = midpoint - 1
        elif current_name[0] < target[0]:
            left = midpoint + 1
        else:
            right = midpoint - 1

    return -1


def main():
    myList = [
        "Bob", "Charlie", "Eva", "Alice", "Grace", "David", "Smith", "Frank", "Zoe", "Jack"
    ]
    sortedList = sorted(myList)

    print("call binarySearch")
    locatedIndex = binarySearch("Smith", sortedList)
    print(sortedList)
    print(locatedIndex, sortedList[locatedIndex])

    print("call dictSearch")
    locatedIndex = dictSearch("Smith", sortedList)
    print(sortedList)
    print(locatedIndex, sortedList[locatedIndex])


if __name__ == "__main__":
    main()

# 运算结果：
# call binarySearch
#  left  midpoint     right
#     0         4         9
#     5         7         9
#     8         8         9
# ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Jack', 'Smith', 'Zoe']
# 8 Smith
# call dictSearch
#  left  midpoint     right
#     0         4         9
#     5         7         9
#     8         8         9
# ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Jack', 'Smith', 'Zoe']
# 8 Smith

