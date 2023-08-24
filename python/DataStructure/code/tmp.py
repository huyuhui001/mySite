myList1 = [2, 4, 8]
myList2 = list(myList1)
print(myList1 is myList2)  # False
print(myList1 == myList2)  # True

myList1.append(10)
myList1.remove(4)
print(myList1)
print(myList2)



