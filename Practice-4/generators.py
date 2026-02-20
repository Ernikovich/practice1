# Generators allow you to iterate over data without storing the entire dataset in memory.
# Instead of using return, generators use the yield keyword.
def my_generator():
  yield 1
  yield 2
  yield 3
for value in my_generator():
  print(value)

def count_up_to(n):
  count = 1
  while count <= n:
    yield count
    count += 1
for num in count_up_to(5):
  print(num)

def large_sequence(n):
  for i in range(n):
    yield i
# This doesn't create a million numbers in memory
gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen))


nums = [10, 20, 30]
it = iter(nums)
print(next(it))  # 10
print(next(it))  # 20
# iter() — это функция, которая превращает коллекцию (список, кортеж, строку и т.д.) в итератор.

for x in iter([1, 2, 3]):
    print(x)

def fibonacci():
  a, b = 0, 1
  while True:
    yield a
    a, b = b, a + b
# Get first 100 Fibonacci numbers
gen = fibonacci()
for _ in range(100):
  print(next(gen))

# The send() method allows you to send a value to the generator:
def echo_generator():
  while True:
    received = yield
    print("Received:", received)
gen = echo_generator()
next(gen) # Prime the generator
gen.send("Hello")
gen.send("World")

# The close() method stops the generator:
def my_gen():
  try:
    yield 1
    yield 2
    yield 3
  finally:
    print("Generator closed")
    # finally — это блок кода, который выполняется всегда, независимо от того, была ошибка или нет.

gen = my_gen()
print(next(gen)) #Генератор запускается до первого yield
gen.close()