print(10 > 9)
print(10 == 9)
print(10 < 9)

a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

s1 = "hello"
s2 = "world!!!"
print(len(s1) == len(s2))
print(len(s1) < len(s2))

nums = [1, 2, 3, 4]
print(3 in nums)
print(10 in nums)

x = None
y = None
print(x is None)
print(x is y)

x = ["apple", "banana"]
y = ["apple", "banana"]
z = x
print(x is z)
print(x is y)
print(x == y)

x = ["apple", "banana"]
y = ["apple", "banana"]
print(x is not y)