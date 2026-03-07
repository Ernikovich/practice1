names = ["Ali", "Dana", "Aruzhan"]
scores = [85, 90, 78]

# enumerate
for index, name in enumerate(names):
    print(index, name)

# zip
for name, score in zip(names, scores):
    print(name, score)

# sorted
print(sorted(scores))

# type conversion
a = "10"
b = int(a)
print(type(b))

fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

keys = ["name", "age", "city"]
values = input("Введите данные через пробел: ").split()  # ['Ali', '20', 'Almaty']
my_dict = dict(zip(keys, values))
print(my_dict)


# zip() объединяет несколько списков ('Ali', 85)
# enumerate() даёт индекс + элемент (0, 'Ali')