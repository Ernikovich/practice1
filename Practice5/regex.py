# re.search() — найти первое совпадение
import re

text = "The rain in Spain"
x = re.search("Spain", text)

print(x.group())   # Spain
print(x.start())   # позиция начала