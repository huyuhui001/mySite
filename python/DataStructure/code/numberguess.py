import random

def main():
    smaller = int(input("输入最小值: "))
    larger = int(input("输入最大值: "))
    myNumber = random.randint(smaller, larger)
    count = 0
    while True:
        count += 1
        userNumber = int(input("输入你猜的值: "))
        if userNumber < myNumber:
            print("你猜的太小！")
        elif userNumber > myNumber:
            print("你猜的太大！")
        else:
            print("恭喜，你在第", count, "次猜对了!")
            break

if __name__ == "__main__":
    main()