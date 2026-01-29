i = 1
while i < 6:
  print(i)
  i += 1

i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

total = 0
n = 1
while n <= 5:
    total += n
    n += 1
print("sum =", total)


attempts = 0
max_attempts = 3
while attempts < max_attempts:
    attempts += 1
print("attempts =", attempts)


items = [1, 2, 3]
while items:
    print("pop", items.pop())
# функция print получает то число, которое «выпрыгнуло» из списка, и показывает его вам на экране.