money = float(input())
count = 0

while money < 700000:
    money *= 1.071
    count += 1

print(count)
