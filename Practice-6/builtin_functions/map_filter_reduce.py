from functools import reduce
numbers=[1,2,3,4,5]
# map
squares = list(map(lambda x: x**2, numbers))
print(squares)
# map — применяет функцию ко всем элементам

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)
# filter — оставляет только элементы, которые подходят

# reduce
sum_numbers = reduce(lambda x, y: x + y, numbers)
print(sum_numbers)
# reduce — сворачивает список в одно значение
