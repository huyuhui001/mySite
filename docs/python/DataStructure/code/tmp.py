print(1*2*3*4*5*6*7*8*9*10)

# =================
result = 1
value = 1

while value <= 10:
    result *= value
    value += 1

print(result, value)

# =================
result = 1
value = 1

for value in range(1, 11):
    result *= value
    value += 1

print(result, value)

# =================
print("Greater"[1])
print("Greater"[-3])
print("Hello" + "Python")
print('A' > 'a')
print('A' < 'a')

# =================
print("Greater"[:])     # 返回字串 Greater 
print("Greater"[2:])    # 返回字串 eater
print("Greater"[:2])    # 返回字串 Gr
print("Greater"[2:5])   # 返回字串 eat

# =================
print("%6s" % "four")
print("%-6s" % "four")
#   four
# four

for i in range(7, 11):
    print(i, 10*i)
# 7 70
# 8 80
# 9 90
# 10 100

for i in range(7, 11):
    print("%-3d%5d" % (i, 10*i))
# 7     70
# 8     80
# 9     90
# 10   100

for i in range(7, 11):
    print("%-3d%5.3f" % (i, i/3))
# 7  2.333
# 8  2.667
# 9  3.000
# 10 3.333

print("%6.3f" % 3.14)
#  3.140
print("%-6.3f" % 3.14)
# 3.140
print(3.14)


salary = 100.00
print("Salary: $" + str(salary))
# Salary: $100.0
print("Salary: $%0.2f" % salary)
# Salary: $100.00




















