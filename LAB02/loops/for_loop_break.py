for i in range(1, 10):
    if i == 4:
        break
    print(i)

nums = [2, 4, 6, 7, 8]
for n in nums:
    if n == 7:
        print("found 7")
        break

words = ["hi", "stop", "bye"]
for w in words:
    if w == "stop":
        break
    print(w)

for i in range(10):
    if i * i > 20:
        print("square too big:", i*i)
        break

text = "abcdefg"
for ch in text:
    if ch == "d":
        break
    print(ch)