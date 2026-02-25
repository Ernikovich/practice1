# re.search() — найти первое совпадение
import re

text = "The rain in Spain"
x = re.search("Spain", text)

print(x.group())   # Spain
print(x.start())   # позиция начала

# re.findall() — найти ВСЕ совпадения
import re
text = "My numbers: 12 and 45"
x = re.findall(r"\d+", text)
print(x)   # ['12', '45']
# \d+ → одна или больше цифр

# re.match() — ищет ТОЛЬКО в начале строки
import re
text = "Hello world"
x = re.match("Hello", text)
print(x.group())   # Hello
# Если строка начинается не с шаблона — вернёт None

# re.split() — разделить строку
import re
text = "apple,banana,orange"
x = re.split(",", text)
print(x)   # ['apple', 'banana', 'orange']

# re.sub() — заменить
import re
text = "I like cats"
x = re.sub("cats", "dogs", text)
print(x)   # I like dogs