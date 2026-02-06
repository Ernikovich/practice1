class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)
#Use the Person class to create an object, and then execute the printname method:
x = Person("John", "Doe")
x.printname()
# class Student(Person): #Create a class named Student, which will inherit the properties and methods from the Person class:
#   pass
# x = Student("Mike", "Olsen")
# x.printname()

# class Student(Person):
#   def __init__(self, fname, lname):
#     Person.__init__(self, fname, lname)

class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)

x = Student("Mike", "Olsen")
x.printname()



class Person:
    def __init__(self, name):
        self.name = name
class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)   # имя берём у родителя
        self.grade = grade      # своё новое свойство



class Animal:
    def __init__(self, name: str):
        self.name = name
    def speak(self) -> str:
        return "Some sound"
class Cat(Animal):
    def speak(self) -> str:
        return "Meow"
class Dog(Animal):
    def speak(self) -> str:
        return "Woof"
if __name__ == "__main__":
    animals = [Cat("Murka"), Dog("Rex"), Animal("Unknown")]
    for a in animals:
        print(a.name, "says:", a.speak())