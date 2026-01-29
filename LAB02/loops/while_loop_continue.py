i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

i = 0
while i < 6:
    i += 1
    if i % 2 == 0:
        continue
    print("odd:", i)

nums = [3, -1, 5, -2, 7]
i = 0
while i < len(nums):
    if nums[i] < 0:
        i += 1
        continue
    print("non-negative:", nums[i])
    i += 1

i = 0
while i < 10:
    i += 1
    if i % 3 != 0:
        continue
    print("multiple of 3:", i)