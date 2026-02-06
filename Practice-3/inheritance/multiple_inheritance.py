
class Flyable:
    def move(self) -> str:
        return "Flying"


class Swimmable:
    def move(self) -> str:
        return "Swimming"


class Duck(Flyable, Swimmable):
    # If we don't override move(), Python will use MRO:
    # Duck -> Flyable -> Swimmable -> object
    pass


class SuperDuck(Flyable, Swimmable):
    def move(self) -> str:
        # Explicitly combine behaviors
        return f"{Flyable.move(self)} and {Swimmable.move(self)}"


if __name__ == "__main__":
    d = Duck()
    sd = SuperDuck()

    # Example 1: MRO chooses Flyable.move
    print("Duck moves:", d.move())

    # Example 2: manual combination
    print("SuperDuck moves:", sd.move())

    # Example 3: show MRO
    print("Duck MRO:", [cls.__name__ for cls in Duck.mro()])
    # mro() = Method Resolution Order
# Он возвращает список классов:
# [Duck, Flyable, Swimmable, object]
# (не строки — именно классы)

# 🏷 2. cls.__name__
# Каждый класс имеет имя:
# Duck.__name__ → "Duck"
# Flyable.__name__ → "Flyable"