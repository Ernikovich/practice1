numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

words = ["python", "oop", "lambda", "map"]
lengths = list(map(lambda w: len(w), words))
print("Lengths:", lengths)

prices = [1000, 2500, 999]
taxed = list(map(lambda p: round(p * 1.12, 2), prices))
print("With tax:", taxed)

a = [1, 2, 3]
b = [10, 20, 30]
summed = list(map(lambda x, y: x + y, a, b))
print("Element-wise sum:", summed)