i = 1
while i <= 10:
    if i == 5:
        break
    print(i)
    i += 1

nums = [2, 4, 6, 7, 8]
idx = 0
while idx < len(nums):
    if nums[idx] == 7:
        print("found 7")
        break
    idx += 1

x = 100
while x > 0:
    x -= 30
    if x < 50:
        break
print("x =", x)

count = 0
while True:
    count += 1
    if count == 2:
        break
print("count =", count)