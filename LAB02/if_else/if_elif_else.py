a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")

temp = 10
if temp < 0:
    print("Freezing")
elif temp < 15:
    print("Cool")
else:
    print("Warm")

day = "Saturday"
if day == "Monday":
    print("Work")
elif day == "Saturday" or day == "Sunday":
    print("Weekend")
else:
    print("Weekday")


balance = 1200
if balance >= 5000:
    print("VIP")
elif balance >= 1000:
    print("Regular")
else:
    print("Basic")


n = 0
if n > 0:
    print("Positive")
elif n == 0:
    print("Zero")
else:
    print("Negative")