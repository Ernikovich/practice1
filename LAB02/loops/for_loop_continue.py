for i in range(1, 7):
    if i % 2 == 0:
        continue
    print("odd:", i)


items = ["a", "", "b", "", "c"]
for item in items:
    if item == "":
        continue
    print(item)

nums = [1, -2, 3, -4, 5]
for n in nums:
    if n < 0:
        continue
    print("non-negative:", n)

nums = [1, -2, 3, -4, 5]
for n in nums:
    if n < 0:
        continue
    print("non-negative:", n)

for ch in "python":
    if ch == "t":
        continue
    print(ch)