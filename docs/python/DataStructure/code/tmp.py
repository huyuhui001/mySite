# from array import Array


def swap(lyst, i, j):
    """交换元素位置为i和j的元素"""
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp


def mergeSort(lyst):
    # lyst        list being sorted
    # copyBuffer temporary space needed during merge
    copyBuffer = Array(len(lyst))
    mergeSortHelper(lyst, copyBuffer, 0, len(lyst) - 1)


def mergeSortHelper(lyst, copyBuffer, low, high):
    # lyst        list being sorted
    # copyBuffer  temp space needed during merge
    # low, high   bounds of sublist
    # middle      midpoint of sublist
    if low < high:
        middle = (low + high) // 2
        mergeSortHelper(lyst, copyBuffer, low, middle)
        mergeSortHelper(lyst, copyBuffer, middle + 1, high)
        merge(lyst, copyBuffer, low, middle, high)


def merge(lyst, copyBuffer, low, middle, high):
    # lyst          list that is being sorted
    # copyBuffer    temp space needed during the merge process
    # low           beginning of first sorted sublist
    # middle        end of first sorted sublist
    # middle + 1    beginning of second sorted sublist
    # high          end of second sorted sublist
    # Initialize i1 and i2 to the first items in each sublist
    i1 = low
    i2 = middle + 1
    # Interleave items from the sublists into the
    # copyBuffer in such a way that order is maintained.
    for i in range(low, high + 1):
        if i1 > middle:
            copyBuffer[i] = lyst[i2]  # First sublist exhausted
            i2 += 1
        elif i2 > high:
            copyBuffer[i] = lyst[i1]  # Second sublist exhausted
            i1 += 1
        elif lyst[i1] < lyst[i2]:
            copyBuffer[i] = lyst[i1]  # Item in first sublist <
            i1 += 1
        else:
            copyBuffer[i] = lyst[i2]  # Item in second sublist <
            i2 += 1
    for i in range(low, high + 1):  # Copy sorted items back to
        lyst[i] = copyBuffer[i]  # proper position in lyst


def main():
    lyst = [12, 19, 17, 18, 14, 11, 15, 13, 16]
    mergeSort(lyst)

if __name__ == "__main__":
    main()

# 运行结果：
