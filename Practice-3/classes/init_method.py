# __init__ — это специальная функция-конструктор
# Она автоматически вызывается, когда ты создаёшь объект:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)


class Student:
    def __init__(self, name: str, age: int, city: str):
        self.name = name #👉 объект “запоминает” своё имя
        self.age = age #👉 объект “запоминает” свой возраст
        self.city = city #👉 объект “запоминает” свой город

    def introduce(self) -> str:
        return f"My name is {self.name}, I'm {self.age}, from {self.city}."
    
if __name__ == "__main__":  #читается как:
# «Если этот файл — главный, то выполняй код ниже»
    s = Student("Ernar", 17, "Almaty")
    print(s.introduce())