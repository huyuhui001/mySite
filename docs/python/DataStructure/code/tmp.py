import random


def swap(lyst, i, j):
    """交换元素位置为i和j的元素"""
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp


def quicksort(lyst):
    # left的初始值是0
    # right的初始值是列表长度减1
    quicksortHelper(lyst, 0, len(lyst) - 1)


def quicksortHelper(lyst, left, right):
    print(lyst)
    if left < right:
        pivotLocation = partition(lyst, left, right)
        quicksortHelper(lyst, left, pivotLocation - 1)
        quicksortHelper(lyst, pivotLocation + 1, right)


def partition(lyst, left, right):
    """对列表进行分区"""
    # 找到基准元素（pivot），并和最后一个元素互换
    middle = (left + right) // 2
    pivot = lyst[middle]
    lyst[middle] = lyst[right]
    lyst[right] = pivot

    # 设定边界元素（boundary point），初始是第一个元素
    boundary = left
    print("pivot: ", pivot, "boundary: ", lyst[boundary])

    # 把所有小于基准的元素都移动到边界的左边
    for index in range(left, right):
        if lyst[index] < pivot:
            swap(lyst, index, boundary)
            boundary += 1
    
    # 交换基准元素和边界元素
    swap(lyst, right, boundary)
    print(lyst)
    return boundary


def main(size=20, sort=quicksort):
    # lyst = []
    # for count in range(size):
    #     lyst.append(random.randint(1, size + 1))
    lyst = [12, 19, 17, 18, 14, 11, 15, 13, 16]
    # print(lyst)
    sort(lyst)
    # print(lyst)


if __name__ == "__main__":
    main()

# 运行结果：
# [12, 19, 17, 18, 14, 11, 15, 13, 16]
# [11, 12, 13, 14, 15, 16, 17, 18, 19]