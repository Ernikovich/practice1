import json
# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}' #x — это обычная строка в Python (тип str).
# parse x:
y = json.loads(x)
# json.loads() разбирает (parse) JSON-строку и превращает её в Python-объект.
# the result is a Python dictionary:
# Превращается в Python словарь (dict):
print(y["age"])

# Особенности JSON:
# Ключи в двойных кавычках "name"
# Строки тоже в двойных кавычках "John"
# Числа, булевы значения, массивы и объекты можно записывать напрямую

# Convert from Python to JSON:
import json
# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
# convert into JSON:
y = json.dumps(x)
# the result is a JSON string:
print(y)


import json
x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}
# json.dumps(x, indent=4)  
json.dumps(x, indent=4, separators=(". ", " = "))
# json.dumps() — берёт Python-объект и возвращает JSON-строку.
# Параметр indent=4 — делает отступы, чтобы JSON был красиво читаемым.

# separators=(item_sep, key_sep) — меняем разделители в JSON:
# item_sep — разделитель между элементами массива или объектами ("," по умолчанию)
# key_sep — разделитель между ключом и значением (":" по умолчанию)
# Между элементами массива/объекта будет ". " вместо запятой
# Между ключом и значением будет " = " вместо двоеточия


# Если у нас объект:
# x = {"a":1,"b":2}
# То с separators=(". ", " = ") получится:
# {
#     "a" = 1. 
#     "b" = 2
# }
# Записываем JSON в файл
with open("out.json", "w", encoding="utf-8") as f:
    data = {"ok": True, "nums": [1, 2, 3]}
    json.dump(data, f, ensure_ascii=False, indent=2)

# open(..., "w") — открываем файл на запись.
# json.dump(data, f, ...) — записываем Python-объект data прямо в файл как JSON.
# ensure_ascii=False — сохраняем русские буквы и символы корректно, а не в виде \uXXXX.
# indent=2 — красиво форматируем в файле.

# Читаем JSON из файла
import json
with open("out.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded)

# f — это переменная, которая теперь ссылается на открытый файл.