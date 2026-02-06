students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

words=["apple","banana","chips","crokant"]
sorted_words=sorted(words,key=lambda w:len(w))
print(sorted_words)

students = [
    {"name": "Ernar", "score": 100},
    {"name": "Alihan", "score": 95},
    {"name": "Aruzhan", "score": 88},
    {"name": "Daniyar", "score": 70},
]
by_score = sorted(students, key=lambda s: s["score"])
print("By score:", by_score)

by_score_desc = sorted(students, key=lambda s: s["score"], reverse=True)
print("By score desc:", by_score_desc)

by_name = sorted(students, key=lambda s: s["name"].lower())
print("By name:", by_name)