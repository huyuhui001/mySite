"""
- 编写一个程序，使之能够接收球体的半径（浮点数），并且可以输出球体的直径、周长、表面积以及体积。
"""

################################ 方法1
# PAI = 3.14
# radius = float(input("输入球半径："))

# diameter = radius * 2
# circumference = 2 * PAI * radius
# surfaceArea = 4 * PAI * radius ** 2
# sphereVolume = 4 * (PAI * radius ** 3) / 3

# print("球半径：", radius, "球直径：", diameter, "球表面积：", surfaceArea, "球体积：", sphereVolume)
# # 运行结果：
# # 输入球半径：3.5
# # 球半径： 3.5 球直径： 7.0 球表面积： 153.86 球体积： 179.50333333333333





################################ 方法2
# import math

# def main():
#     try:
#         radius = float(input("请输入球半径："))
#         if radius <= 0:
#             print("半径必须为正数！")
#             return

#         diameter = 2 * radius
#         circumference = 2 * math.pi * radius
#         surfaceArea = 4 * math.pi * radius ** 2
#         volume = (4/3) * math.pi * radius ** 3

#         print(f"球体的直径：{diameter:.2f}")
#         print(f"球体的周长：{circumference:.2f}")
#         print(f"球体的表面积：{surfaceArea:.2f}")
#         print(f"球体的体积：{volume:.2f}")
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()

# # 运行结果：
# # 请输入球半径：3.5
# # 球体的直径：7.00
# # 球体的周长：21.99
# # 球体的表面积：153.94
# # 球体的体积：179.59



################################ 方法3
# import math

# class Sphere:
#     def __init__(self, radius):
#         self.radius = radius

#     def diameter(self):
#         return 2 * self.radius

#     def circumference(self):
#         return 2 * math.pi * self.radius

#     def surfaceArea(self):
#         return 4 * math.pi * self.radius ** 2

#     def volume(self):
#         return (4/3) * math.pi * self.radius ** 3

# def main():
#     try:
#         radius = float(input("请输入球体的半径："))
#         if radius <= 0:
#             print("半径必须为正数！")
#             return

#         sphere = Sphere(radius)

#         print(f"球体的直径：{sphere.diameter():.2f}")
#         print(f"球体的周长：{sphere.circumference():.2f}")
#         print(f"球体的表面积：{sphere.surfaceArea():.2f}")
#         print(f"球体的体积：{sphere.volume():.2f}")
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()


# # 运行结果：
# # 请输入球体的半径：3.5
# # 球体的直径：7.00
# # 球体的周长：21.99
# # 球体的表面积：153.94
# # 球体的体积：179.59




"""
- 员工的周工资等于小时工资乘以正常的总工作时间再加上加班工资。加班工资等于总加班时间乘以小时工资的1.5倍。
编写一个程序，让用户可以输入小时工资、正常的总工作时间以及加班总时间，然后显示出员工的周工资。
"""
################################ 方法1
# hourSalary = float(input("输入小时工资（元）："))
# totalWorkingHours = float(input("输入本周正常总工作时间（小时）："))
# totalOvertimeHours = float(input("输入本周总加班总工作时间（小时）："))
# weeklySalary = hourSalary * totalWorkingHours + hourSalary * totalOvertimeHours * 1.5

# print("员工的周工资（元）是：", weeklySalary)
# # 运行结果：
# # 输入小时工资（元）：20
# # 输入每周正常总工作时间（小时）：40
# # 输入每周总加班总工作时间（小时）：10
# # 员工的周工资（元）是： 1100.0


################################ 方法2
# def calculate_weekly_salary(hourly_wage, normal_hours, overtime_hours):
#     overtime_pay = overtime_hours * hourly_wage * 1.5
#     normal_pay = normal_hours * hourly_wage
#     weekly_salary = normal_pay + overtime_pay
#     return weekly_salary

# def main():
#     try:
#         hourly_wage = float(input("请输入小时工资："))
#         normal_hours = float(input("请输入正常的总工作时间（小时）："))
#         overtime_hours = float(input("请输入加班总时间（小时）："))

#         weekly_salary = calculate_weekly_salary(hourly_wage, normal_hours, overtime_hours)
#         print(f"员工的周工资为：{weekly_salary:.2f}")
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()

# # 运行结果：
# # 请输入小时工资：20
# # 请输入正常的总工作时间（小时）：40
# # 请输入加班总时间（小时）：10
# # 员工的周工资为：1100.00



################################ 方法3
# class Employee:
#     def __init__(self, hourly_wage, normal_hours, overtime_hours):
#         self.hourly_wage = hourly_wage
#         self.normal_hours = normal_hours
#         self.overtime_hours = overtime_hours

#     def calculate_weekly_salary(self):
#         overtime_pay = self.overtime_hours * self.hourly_wage * 1.5
#         normal_pay = self.normal_hours * self.hourly_wage
#         weekly_salary = normal_pay + overtime_pay
#         return weekly_salary

# def main():
#     try:
#         hourly_wage = float(input("请输入小时工资："))
#         normal_hours = float(input("请输入正常的总工作时间（小时）："))
#         overtime_hours = float(input("请输入加班总时间（小时）："))

#         employee = Employee(hourly_wage, normal_hours, overtime_hours)
#         weekly_salary = employee.calculate_weekly_salary()
#         print(f"员工的周工资为：{weekly_salary:.2f}")
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()

# # 运行结果：
# # 请输入小时工资：20
# # 请输入正常的总工作时间（小时）：40
# # 请输入加班总时间（小时）：10
# # 员工的周工资为：1100.00





"""
- 有一个标准的科学实验：扔一个球，看看它能反弹多高。一旦确定了球的“反弹高度”，这个比值就给出了相应的反弹度指数。
例如，如果从10ft（1ft=0.3048m）高处掉落的球可以反弹到6 ft高，那么相应的反弹度指数就是0.6；在一次反弹之后，球的总行进距离是16 ft。接下来，球继续弹跳，那么两次弹跳后的总距离应该是：10 ft + 6 ft + 6 ft + 3.6 ft = 25.6 ft。可以看到，每次连续弹跳所经过的距离是：球到地面的距离，加上这个距离乘以 0.6，这时球又弹回来了。编写一个程序，可以让用户输入球的初始高度和允许球弹跳的次数，并输出球所经过的总距离。
"""
################################ 方法1
# height = float(input("输入小球初始高度（ft）："))
# times = float(input("输入允许小球弹跳次数："))
# distance = 0
# traceDistance = 0

# while times:
#     distance = height + 0.6 * height
#     traceDistance += distance
#     height = 0.6 * height
#     times -= 1

# print("小球经过的总距离（ft）：", traceDistance)
# # 运行结果：
# # 输入小球初始高度（ft）：50
# # 输入允许小球弹跳次数：5
# # 小球经过的总距离（ft）： 184.448
# # 输入小球初始高度（ft）：100
# # 输入允许小球弹跳次数：10
# # 小球经过的总距离（ft）： 397.58135296000006

################################ 方法2
# def calculate_total_distance(initial_height, num_bounces):
#     rebound_factor = 0.6
#     total_distance = 0
#     height = initial_height

#     for _ in range(num_bounces + 1):
#         total_distance += height
#         height *= rebound_factor

#     return total_distance

# def main():
#     try:
#         initial_height = float(input("请输入球的初始高度（单位：ft）："))
#         num_bounces = int(input("请输入允许球弹跳的次数："))

#         total_distance = calculate_total_distance(initial_height, num_bounces)
#         print(f"球所经过的总距离为：{total_distance:.2f} ft")
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()

# # 运行结果：
# # 请输入球的初始高度（单位：ft）：50
# # 请输入允许球弹跳的次数：5
# # 球所经过的总距离为：119.17 ft
# # 请输入球的初始高度（单位：ft）：100
# # 请输入允许球弹跳的次数：10
# # 球所经过的总距离为：249.09 ft


################################ 方法3
# class BouncingBall:
#     def __init__(self, initial_height, num_bounces):
#         self.initial_height = initial_height
#         self.num_bounces = num_bounces
#         self.rebound_factor = 0.6

#     def calculate_total_distance(self):
#         total_distance = 0
#         height = self.initial_height

#         for _ in range(self.num_bounces + 1):
#             total_distance += height
#             height *= self.rebound_factor

#         return total_distance

# def main():
#     try:
#         initial_height = float(input("请输入球的初始高度（单位：ft）："))
#         num_bounces = int(input("请输入允许球弹跳的次数："))

#         bouncing_ball = BouncingBall(initial_height, num_bounces)
#         total_distance = bouncing_ball.calculate_total_distance()
#         print(f"球所经过的总距离为：{total_distance:.2f} ft")
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()


# # 运行结果：
# # 请输入球的初始高度（单位：ft）：50
# # 请输入允许球弹跳的次数：5
# # 球所经过的总距离为：119.17 ft
# # 请输入球的初始高度（单位：ft）：100
# # 请输入允许球弹跳的次数：10
# # 球所经过的总距离为：249.09 ft



"""
- 德国数学家Gottfried Leibniz发明了下面这个用来求π的近似值的方法：`π/4 = 1 - 1/3 + 1/5 - 1/7 + ......`，请编写一个程序，让用户可以指定这个近似值所使用的迭代次数，并且显示出结果。
"""

################################ 方法1
# n = int(input("输入迭代次数："))
# mySum = 0

# while n:
#     mySum += 1 / (2 * n - 1) * ((-1)**(n + 1))
#     n -= 1

# print("π的近似值是：", mySum * 4)

# # 运行结果：
# # 输入迭代次数：5
# # π的近似值是： 3.33968253968254
# # 输入迭代次数：10
# # π的近似值是： 3.0418396189294024
# # 输入迭代次数：20
# # π的近似值是： 3.0916238066678385
# # 输入迭代次数：10000000
# # π的近似值是： 3.1415925535897933

################################ 方法2
# def calculate_pi_approximation(iterations):
#     approximation = 0
#     sign = 1

#     for i in range(1, iterations * 2, 2):
#         approximation += sign * (1 / i)
#         sign *= -1

#     return approximation * 4

# def main():
#     try:
#         iterations = int(input("请输入迭代次数："))

#         if iterations <= 0:
#             print("迭代次数必须为正整数！")
#             return

#         pi_approximation = calculate_pi_approximation(iterations)
#         print(f"π 的近似值为：{pi_approximation:.10f}")
#     except ValueError:
#         print("请输入有效的整数！")

# if __name__ == "__main__":
#     main()


# # 运行结果：
# # 请输入迭代次数：5
# # π 的近似值为：3.3396825397
# # 请输入迭代次数：10
# # π 的近似值为：3.0418396189
# # 请输入迭代次数：20
# # π 的近似值为：3.0916238067
# # 请输入迭代次数：10000000
# # π 的近似值为：3.1415925536


################################ 方法3
# class PiApproximation:
#     @classmethod
#     def calculate_pi_approximation(cls, iterations):
#         approximation = 0
#         sign = 1

#         for i in range(1, iterations * 2, 2):
#             approximation += sign * (1 / i)
#             sign *= -1

#         return approximation * 4

# def main():
#     try:
#         iterations = int(input("请输入迭代次数："))

#         if iterations <= 0:
#             print("迭代次数必须为正整数！")
#             return

#         pi_approximation = PiApproximation.calculate_pi_approximation(iterations)
#         print(f"π 的近似值为：{pi_approximation:.10f}")
#     except ValueError:
#         print("请输入有效的整数！")

# if __name__ == "__main__":
#     main()


# # 运行结果：
# # 输入迭代次数：5
# # π 的近似值为：3.3396825397
# # 请输入迭代次数：10
# # π 的近似值为：3.0418396189
# # 请输入迭代次数：20
# # π 的近似值为：3.0916238067
# # 请输入迭代次数：10000000
# # π 的近似值为：3.1415925536


"""
- 某计算机商店有购买计算机的信贷计划：首付10%，年利率为12%，每月所付款为购买价格减去首付之后的5%。编写一个以购买价格为输入的程序，可以输出一个有适当标题的表格，显示贷款期限内的付款计划。表的每一行都应包含下面各项：

- 月数（以1开头）；
- 当前所欠的余额；
- 当月所欠的利息；
- 当月所欠的本金；
- 当月所需付款金额；
- 付款之后所欠的金额。
一个月的利息等于余额 × 利率/12；一个月所欠的本金等于当月还款额减去所欠的利息。
"""

################################ 方法1
# def calculate_payment_schedule(purchase_price):
#     down_payment = purchase_price * 0.1
#     loan_balance = purchase_price - down_payment
#     annual_interest_rate = 0.12
#     monthly_interest_rate = annual_interest_rate / 12
#     monthly_payment = (purchase_price - down_payment) * 0.05

#     payment_schedule = []

#     for month in range(1, 13):
#         interest = loan_balance * monthly_interest_rate
#         principal = monthly_payment - interest
#         loan_balance -= principal
#         payment_schedule.append((month, loan_balance, interest, principal, monthly_payment, loan_balance + monthly_payment))

#     return payment_schedule

# def main():
#     try:
#         purchase_price = float(input("请输入购买价格："))

#         payment_schedule = calculate_payment_schedule(purchase_price)

#         print("{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
#             "月数", "当前所欠的余额", "当月所欠的利息", "当月所欠的本金", "当月所需付款金额", "付款之后所欠的金额"))

#         for payment in payment_schedule:
#             month, balance, interest, principal, monthly_payment, new_balance = payment
#             print("{:<10} {:<15.2f} {:<15.2f} {:<15.2f} {:<15.2f} {:<15.2f}".format(
#                 month, balance, interest, principal, monthly_payment, new_balance))
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()


# # 运行结果：
# # 请输入购买价格：5000
# # 月数         当前所欠的余额         当月所欠的利息         当月所欠的本金         当月所需付款金额        付款之后所欠的金额      
# # 1          4320.00         45.00           180.00          225.00          4545.00        
# # 2          4138.20         43.20           181.80          225.00          4363.20        
# # 3          3954.58         41.38           183.62          225.00          4179.58        
# # 4          3769.13         39.55           185.45          225.00          3994.13        
# # 5          3581.82         37.69           187.31          225.00          3806.82        
# # 6          3392.64         35.82           189.18          225.00          3617.64        
# # 7          3201.56         33.93           191.07          225.00          3426.56        
# # 8          3008.58         32.02           192.98          225.00          3233.58        
# # 9          2813.67         30.09           194.91          225.00          3038.67        
# # 10         2616.80         28.14           196.86          225.00          2841.80        
# # 11         2417.97         26.17           198.83          225.00          2642.97        
# # 12         2217.15         24.18           200.82          225.00          2442.15        





################################ 方法2
# class PaymentSchedule:
#     def __init__(self, purchase_price):
#         self.purchase_price = purchase_price
#         self.down_payment = purchase_price * 0.1
#         self.loan_balance = purchase_price - self.down_payment
#         self.annual_interest_rate = 0.12
#         self.monthly_interest_rate = self.annual_interest_rate / 12
#         self.monthly_payment = (purchase_price - self.down_payment) * 0.05

#     def calculate_schedule(self):
#         payment_schedule = []

#         for month in range(1, 13):
#             interest = self.loan_balance * self.monthly_interest_rate
#             principal = self.monthly_payment - interest
#             self.loan_balance -= principal
#             payment_schedule.append((month, self.loan_balance, interest, principal, self.monthly_payment, self.loan_balance + self.monthly_payment))

#         return payment_schedule

#     def print_schedule_table(self):
#         payment_schedule = self.calculate_schedule()

#         print("{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
#             "月数", "当前所欠的余额", "当月所欠的利息", "当月所欠的本金", "当月所需付款金额", "付款之后所欠的金额"))

#         for payment in payment_schedule:
#             month, balance, interest, principal, monthly_payment, new_balance = payment
#             print("{:<10} {:<15.2f} {:<15.2f} {:<15.2f} {:<15.2f} {:<15.2f}".format(
#                 month, balance, interest, principal, monthly_payment, new_balance))

# def main():
#     try:
#         purchase_price = float(input("请输入购买价格："))

#         payment_schedule = PaymentSchedule(purchase_price)
#         payment_schedule.print_schedule_table()
#     except ValueError:
#         print("请输入有效的数字！")

# if __name__ == "__main__":
#     main()

# # 运行结果
# # 请输入购买价格：5000
# # 月数         当前所欠的余额         当月所欠的利息         当月所欠的本金         当月所需付款金额        付款之后所欠的金额      
# # 1          4320.00         45.00           180.00          225.00          4545.00        
# # 2          4138.20         43.20           181.80          225.00          4363.20        
# # 3          3954.58         41.38           183.62          225.00          4179.58        
# # 4          3769.13         39.55           185.45          225.00          3994.13        
# # 5          3581.82         37.69           187.31          225.00          3806.82        
# # 6          3392.64         35.82           189.18          225.00          3617.64        
# # 7          3201.56         33.93           191.07          225.00          3426.56        
# # 8          3008.58         32.02           192.98          225.00          3233.58        
# # 9          2813.67         30.09           194.91          225.00          3038.67        
# # 10         2616.80         28.14           196.86          225.00          2841.80        
# # 11         2417.97         26.17           198.83          225.00          2642.97        
# # 12         2217.15         24.18           200.82          225.00          2442.15



"""
- 财务部门在文本文件里保存了所有员工在每个工资周期里的信息列表。文件中每一行的格式为`<last name> <hourly wage> <hours worked>`。请编写一个程序，让用户可以输入文件的名称，并在终端上打印出给定时间内支付给每个员工的工资报告。这个报告是一个有合适标题的表，其中每行都应该包含员工的姓名、工作时长以及给定时间内所支付的工资。
"""

################################ 方法1

# # 程序会提示用户输入文件名，然后读取文件中的员工信息，计算工资报告，并打印出员工的姓名、工作时长和支付工资。注意，程序会检查文件是否存在，并会对文件中的每行数据进行处理以确保正确解析。
# class Employee:
#     def __init__(self, last_name, hourly_wage, hours_worked):
#         self.last_name = last_name
#         self.hourly_wage = float(hourly_wage)
#         self.hours_worked = float(hours_worked)

#     def calculate_salary(self):
#         return self.hourly_wage * self.hours_worked

# def main():
#     try:
#         filename = input("请输入文件名：")

#         with open(filename, 'r') as file:
#             employees = []
#             for line in file:
#                 parts = line.strip().split()
#                 if len(parts) == 3:
#                     last_name, hourly_wage, hours_worked = parts
#                     employee = Employee(last_name, hourly_wage, hours_worked)
#                     employees.append(employee)

#         print("{:<20} {:<15} {:<15}".format("员工姓名", "工作时长", "支付工资"))
#         print("=" * 50)

#         total_salary = 0

#         for employee in employees:
#             salary = employee.calculate_salary()
#             total_salary += salary
#             print("{:<20} {:<15.2f} {:<15.2f}".format(
#                 employee.last_name, employee.hours_worked, salary))

#         print("=" * 50)
#         print(f"总支付工资：{total_salary:.2f}")
#     except FileNotFoundError:
#         print("文件不存在！")

# if __name__ == "__main__":
#     main()





"""
- 统计学家希望使用一组函数计算数字列表的中位数（median）和众数（mode）。中位数是指如果对列表进行排序将会出现在列表中点的数字，众数是指列表中最常出现的数字。把这些功能定义在名叫stats.py的模块中。除此之外，模块还应该包含一个名叫mean的函数，用来计算一组数字的平均值。每个函数都会接收一个数字列表作为参数，并返回一个数字。
"""
"""
- 编写程序，让用户可以浏览文件里的文本行。这个程序会提示用户输入文件名，然后把文本行都输入列表。接下来，这个程序会进入一个循环，在这个循环里打印出文件的总行数，并提示用户输入行号。这个行号的范围应当是1到文件的总行数。如果输入是0，那么程序退出；否则，程序将打印出行号所对应的文本行。
"""
"""
- 在本章讨论的numberguess程序里，计算机会“构思”一个数字，而用户则输入猜测的值，直到猜对为止。编写这样一个程序，使其可以调换这两个角色，也就是：用户去“构思”一个数字，然后计算机去计算并输出猜测的值。和前面那个游戏版本一样，当计算机猜错时，用户必须给出相应的提示，例如“<”和“>”（分别代表“我的数字更小”和“我的数字更大”）。当计算机猜对时，用户应该输入“=”。用户需要在程序启动的时候输入数字的下限和上限。计算机应该在最多`[log2(high−low)+1]`次猜测里找到正确的数字。程序应该能够跟踪猜测次数，如果猜测错误的次数到了允许猜测的最大值但还没有猜对，就输出消息“You're cheating！”。下面是和这个程序进行交互的示例：

```python
Enter the smaller number: 1
Enter the larger number: 100
Your number is 50
Enter =, <, or >: >
Your number is 75
Enter =, <, or >: <
Your number is 62
Enter =, <, or >: <
Your number is 56
Enter =, <, or >: =
Hooray, I've got it in 4 tries!
```
"""





"""
- 有一个简单的课程管理系统，它通过使用名字和一组考试分数来模拟学生的信息。这个系统应该能够创建一个具有给定名字和分数（起初均为0）的学生对象。系统应该能够访问和替换指定位置处的分数（从0开始计数）、得到学生有多少次考试、得到的最高分、得到的平均分以及学生的姓名。除此之外，在打印学生对象的时候，应该像下面这样显示学生的姓名和分数：

```python
Name: Ken Lambert
Score 1: 88
Score 2: 77
Score 3: 100
```

请定义一个支持这些功能和行为的Student类，并且编写一个创建Student对象并运行其方法的简短的测试函数。
"""
