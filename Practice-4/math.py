x = min(5, 10, 25)
y = max(5, 10, 25)
print(x)
print(y)

x = abs(-7.25)
print(x)

x = pow(4, 3)
print(x)

import math
x = math.sqrt(64)
print(x)

import math
x = math.ceil(1.4)
y = math.floor(1.4)
print(x) # returns 2
print(y) # returns 1



import math
x = math.pi
print(x)
print(round(3.14159, 2))

import random
# random module
a = [-5, 2, 10, 3]
print(random.random())          # 0..1
# Возвращает случайное число с плавающей точкой от 0 (включительно) до 1 (не включительно)
print(random.randint(1, 10))    # 1..10
# Возвращает случайное целое число от 1 до 10 включительно.
print(random.choice(a))         # random element
# Выбирает случайный элемент из списка a.

b = [1, 2, 3, 4, 5]
random.shuffle(b)
# shuffle перемешивает элементы списка на месте, то есть изменяет сам список b.
print(b)