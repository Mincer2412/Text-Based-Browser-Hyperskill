numbers = list()
s = 0

while True:
    n = int(input())
    s += n
    numbers.append(n)

    if s == 0:
        break

total = 0

for i in numbers:
    total += i**2

print(total)
