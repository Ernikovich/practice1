class Person:
    def __init__(self, name: str):
        self.name = name

    def info(self) -> str:
        return f"Name: {self.name}"
    

class Student(Person):
    def __init__(self, name: str, grade: int):
        super().__init__(name)  # call parent's constructor
        self.grade = grade
    def info(self) -> str:
        # call parent's method and extend result
        base = super().info()
        return f"{base}, Grade: {self.grade}"
    
if __name__ == "__main__":
    s = Student("Ernar", 11)
    print(s.info())