a = 5
b = 2
if a > b: print("a is greater than b")

a = 2
b = 330
print("A") if a > b else print("B")

a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
# В display_name положи username, ЕСЛИ username не пустой,
# ИНАЧЕ положи "Guest"

#result = A if CONDITION else B
# 📌 A — когда условие True
# 📌 B — когда False