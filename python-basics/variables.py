x=5 #integer 
y="John" #string
print(x)
print(y)

x=4 # x is of type int
x="Sally" # x is now of type str
print(x)


#You can get the data type of a variable with the type() function.
x = 5
y = "John"
print(type(x))
print(type(y))


x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#If you have a collection of values in a list, tuple etc. Python allows you to extract the values into variables. This is called unpacking.
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)


x="awesome"
def myFunc():
    x="fantastic"
    print("Python is " + x)
myFunc()
print("Python is "+x)