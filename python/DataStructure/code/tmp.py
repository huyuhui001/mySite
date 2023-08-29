class SavingsAccount(object):
    """返回储蓄账户的所有人名字、PIN码、余额"""

    def __init__(self, name, pin, balance=0.0):
        self.name = name
        self.pin = pin
        self.balance = balance

    def __lt__(self, other):
        return self.name < other.name

    # Other methods, including __eq__


def main():
    s1 = SavingsAccount("Ken", "1001", 0)
    s2 = SavingsAccount("Bill", "1001", 30)
    s3 = SavingsAccount("Ken", "1000", 0)
    s4 = s1

    print("s1 < s2: ", s1 < s2)
    print("s2 < s1: ", s2 < s1)
    print("s2 > s1: ", s2 > s1)
    print("s2 == s1: ", s2 == s1)
    print("s1 == s3: ", s1 == s3)
    print("s1 == s4: ", s1 == s4)


if __name__ == "__main__":
    main()

# 运算结果：
# s1 < s2:  False
# s2 < s1:  True
# s2 > s1:  False
# s2 == s1:  False
# s1 == s3:  False
# s1 == s4:  True