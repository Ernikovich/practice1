class MyClass:
  x = 5
p1 = MyClass()
print(p1.x)
# You can delete objects by using the del keyword:
del p1

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()
print(p1.x)
print(p2.x)
print(p3.x)

class Wolf:
  def bark(self):
    print("Woof")

class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def multiply(self, a: float, b: float) -> float:
        return a * b

if __name__ == "__main__":
    # Example 1: create an object and call method
    d = Wolf()
    d.bark()

    # Example 2: another class
    calc = Calculator()
    print("2 + 5 =", calc.add(2, 5))
    print("3 * 4 =", calc.multiply(3, 4))