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


print("Greater"[:])     # 返回字串 Greater 
print("Greater"[2:])    # 返回字串 eater
print("Greater"[:2])    # 返回字串 Gr
print("Greater"[2:5])   # 返回字串 eat




