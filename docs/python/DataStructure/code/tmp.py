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


def letter_position(myLetter):
    letter = myLetter.lower()  # 转成小写字母
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    if letter in alphabet:
        return alphabet.index(letter) + 1  # 位置按1～26计算
    else:
        return None  # 非字母


def dictSearch(target, sortedLyst):
    left = 0
    right = len(sortedLyst) - 1

    # 首字母在字母表中的百分位
    letter_position_range = letter_position(target[0]) * 100 // 26
    # 按照所得的首字母在字母表中的百分位，作为给定字串中设定搜索起始百分位
    midpoint = letter_position_range * (len(sortedLyst) - 1) // 100

    print("%5s%10s%10s" % ("left", "midpoint", "right"))

    while left <= right:
        print("%5s%10s%10s" % (left, midpoint, right))

        if target == sortedLyst[midpoint]:
            return midpoint
        elif target < sortedLyst[midpoint]:
            right = midpoint - 1
        else:
            left = midpoint + 1

        midpoint = (left + right) // 2

    return -1


def main():
    myList = [
        "Bob", "Charlie", "Eva", "Alice", "Grace", "David", "Smith", "Frank",
        "Zoe", "Jack"
    ]
    sortedList = sorted(myList)
    print(sortedList)

    print("=====call binarySearch=====")
    locatedIndex = binarySearch("Alice", sortedList)
    print("Found", sortedList[locatedIndex], "in position", locatedIndex)

    print("=====call dictSearch=====")
    locatedIndex = dictSearch("Alice", sortedList)
    print("Found", sortedList[locatedIndex], "in position", locatedIndex)


if __name__ == "__main__":
    main()

# 运算结果：
# 搜索Alice
# ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Jack', 'Smith', 'Zoe']
# =====call binarySearch=====
#  left  midpoint     right
#     0         4         9
#     0         1         3
#     0         0         0
# Found Alice in position 0
# =====call dictSearch=====
#  left  midpoint     right
#     0         0         9
# Found Alice in position 0

# 搜索Bob
# ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Jack', 'Smith', 'Zoe']
# =====call binarySearch=====
#  left  midpoint     right
#     0         4         9
#     0         1         3
# Found Bob in position 1
# =====call dictSearch=====
#  left  midpoint     right
#     0         0         9
#     1         5         9
#     1         2         4
#     1         1         1
# Found Bob in position 1

# 搜索Smith
# ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Jack', 'Smith', 'Zoe']
# =====call binarySearch=====
#  left  midpoint     right
#     0         4         9
#     5         7         9
#     8         8         9
# Found Smith in position 8
# =====call dictSearch=====
#  left  midpoint     right
#     0         6         9
#     7         8         9
# Found Smith in position 8

# 搜索Zoe
# ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Jack', 'Smith', 'Zoe']
# =====call binarySearch=====
#  left  midpoint     right
#     0         4         9
#     5         7         9
#     8         8         9
#     9         9         9
# Found Zoe in position 9
# =====call dictSearch=====
#  left  midpoint     right
#     0         9         9
# Found Zoe in position 9
