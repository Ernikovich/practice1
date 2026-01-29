#Boolean values
print(10 > 9)
print(10 == 9)
print(10 < 9)

a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

print(bool("Hello"))
print(bool(15)) #: В логическом контексте все числа, кроме \(0\) (например, \(1,-5,15,3.14\)), считаются True. 

#The following will return True:
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#The following will return False:
bool(False) 
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})