import random


def swap(lyst, i, j):
    """交换元素位置为i和j的元素"""
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp


def quicksort(lyst):
    quicksortHelper(lyst, 0, len(lyst) - 1)


def quicksortHelper(lyst, left, right):
    if left < right:
        # 检查子列表的大小是否小于50
        if right - left < 50:
            # 如果小于50，使用插入排序
            insertionSort(lyst, left, right)
        else:
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


def insertionSort(lyst, left, right):
    """插入排序算法"""
    for i in range(left + 1, right + 1):
        currentElement = lyst[i]
        j = i
        while j > left and currentElement < lyst[j - 1]:
            lyst[j] = lyst[j - 1]
            j -= 1
        lyst[j] = currentElement


def main(size=20, sort=quicksort):
    lyst = [random.randint(1, size) for _ in range(size)]
    print("Before sorted", lyst)
    sort(lyst)
    print("After sorted", lyst)


if __name__ == "__main__":
    main()

# 运行结果：
# Before sorted [1, 3, 6, 14, 9, 6, 14, 15, 17, 13, 4, 3, 1, 13, 11, 16, 2, 4, 6, 2]
# After sorted [1, 1, 2, 2, 3, 3, 4, 4, 6, 6, 6, 9, 11, 13, 13, 14, 14, 15, 16, 17]