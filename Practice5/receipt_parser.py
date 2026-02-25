import re
import json
with open("raw.txt","r") as f:
    text=f.read()

# f — это просто переменная.
# Она хранит файл, который мы открыли.

prices=re.findall(r"\b\d+\b",text)
# \b Это граница слова (word boundary).
# \d  \d = любая цифра То же самое что [0-9]  + = один или больше
print(prices)

products=re.findall(r"([A-Za-a]+)\s+\d+",text)
# Круглые скобки = группа Они позволяют: выделить часть совпадения потом получить её через group(1)
# [A-Za-z] Квадратные скобки = набор символов.      + = один или больше
# \s = пробел  + = один или больше           \d = цифра        + = одна или больше
# ([A-Za-z]+)   → Milk
# \s+           → пробел
# \d+           → 450

total=sum(map(int,prices))

date=re.search(r"\d{2}/\d{2}/\d{4}", text)
# \d = любая цифра (0–9)   \d{2}ровно 2 цифры      2 цифры (день)
# \d{2}  2 цифры (месяц)
# / → буквально символ /
# \d{4}  4 цифры (год)
# Формат: 24/02/2026
time = re.search(r"\d{2}:\d{2}", text)
# print(date.group())
# print(time.group())

payment=re.search(r"Payment:\s+(\w+)", text)
# Просто ищем буквальный текст "Payment:" в строке.
# \s+ \s → любой пробельный символ (пробел, табуляция, перенос строки).  + → один или больше таких символов.
# (\w+)
# \w → буква, цифра или нижнее подчеркивание (A-Z, a-z, 0-9, _)       + → один или больше символов   () → группа, которую можно получить через .group(1)
# .group(1) даёт содержимое первой группы () — в нашем случае метод оплаты.

result = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date.group() if date else None,
    "time": time.group() if time else None,
    "payment": payment.group(1) if payment else None
}
# re.search() возвращает объект Match, если совпадение есть, или None, если нет.

print(json.dumps(result, indent=4))
# json.dumps() превращает словарь Python в строку JSON, которую можно красиво распечатать.

# indent=4 → делает отступ 4 пробела, чтобы JSON было легко читать.