# The filter() function creates a list of items for which a function returns True
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

numbers = list(range(1, 21))
gt_10 = list(filter(lambda x: x > 10, numbers))
print("> 10:", gt_10)

words = ["cat", "house", "python", "oop", "study"]
long_words = list(filter(lambda w: len(w) > 4, words))
print("Long words:", long_words)

scores = [120, 90, -5, 70, 101, 50]
valid=list(filter(lambda s:0<=s<=100,scores))
print("Valid scores: ",valid)