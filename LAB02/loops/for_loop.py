fruits = ["apple", "banana", "cherry"]
for f in fruits:
    print(f)

for i in range(3):
    print("i =", i)

for ch in "Python":
    print(ch)

person = {"name": "Ernar", "age": 18}
for key in person:
    print(key, "=", person[key])


names = ["Alihan", "Ernar", "Aruzhan"]
for idx, name in enumerate(names):
    print(idx, name)

# (0, "Alihan")
# (1, "Ernar")
# (2, "Aruzhan")