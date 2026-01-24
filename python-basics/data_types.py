# Text Type:	str
# Numeric Types:	int, float, complex
# Sequence Types:	list, tuple, range
# Mapping Type:	dict
# Set Types:	set, frozenset
# Boolean Type:	bool
# Binary Types:	bytes, bytearray, memoryview
# None Type:	NoneType

x="Yernar" #str
x = 30	#int	
x = 15.5	#float	
x = 3j	#complex
x = ["Alma", "banana", "qulpunai"]	#list	
x = ("alma", "banana", "aulpunai")	#tuple	
x = range(6)	#range	
x = {"name" : "Yernar", "age" : 17}	#dict	
x = {"apple", "banana", "cherry"}	#set	
x = frozenset({"apple", "banana", "cherry"})	#frozenset	
x = True	#bool	
x = b"Hello"	#bytes	
x = bytearray(5)	#bytearray	
x = memoryview(bytes(5))	#memoryview	
x = None	#NoneType



# str — строка (текст)


x = "Yernar"
print(x, type(x))
print(x.upper())  # "YERNAR"

# int — целое число

x = 30
print(x + 5)      # 35
print(type(x))

# float — дробное число

x = 15.5
print(x * 2)      # 31.0
print(type(x))

# complex — комплексное число

x = 3j
print(x * 2)      # 6j
print(type(x))

# list — список (изменяемый)

# Хранит набор элементов, можно менять.

x = ["alma", "banana", "qulpunai"]
x.append("orange")
x[0] = "apple"
print(x)

# tuple — кортеж (неизменяемый)

# Как список, но менять нельзя (удобно для “фиксированных” данных).

x = ("alma", "banana", "qulpunai")
print(x[1])       # "banana"
# x[0] = "apple"  # ошибка

# range — диапазон чисел

x = range(6)
print(list(x))    # [0, 1, 2, 3, 4, 5]

# dict — словарь (ключ → значение)

# Данные по “именам” (ключам).

x = {"name": "Yernar", "age": 17}
print(x["name"])      # "Yernar"
x["age"] = 18
print(x)

# set — множество (уникальные элементы, без порядка)

# Убирает повторы, быстро проверяет “есть ли элемент”.

x = {"apple", "banana", "cherry", "banana"}
print(x)              # "banana" будет один раз
print("apple" in x)   # True

# frozenset — “замороженное” множество (неизменяемое)

# Как set, но менять нельзя.

x = frozenset({"apple", "banana"})
print("apple" in x)   # True
# x.add("cherry")     # ошибка

# bool — логическое значение (True/False)


x = True
print(5 > 2)          # True
print(type(x))

# bytes — байты (неизменяемые)

# Для данных “как в файлах/сети”, бинарные данные.

x = b"Hello"
print(x[0])           # 72 (код 'H')
print(type(x))

# bytearray — массив байт (изменяемый)

# Как bytes, но можно менять.

x = bytearray(5)      # 5 нулевых байт
x[0] = 65             # 'A'
print(x)

# memoryview — “окно” на байты без копирования

# Чтобы работать с большим байтовым массивом эффективно.

data = bytes(5)
x = memoryview(data)
print(x[0])           # 0
print(type(x))

# NoneType (None) — “ничего / пусто”

x = None
print(x is None)      # True
print(type(x))