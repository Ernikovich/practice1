class Vehicle:
    def start(self) -> str:
        return "Vehicle started"

    def fuel_type(self) -> str:
        return "Unknown fuel"


class ElectricCar(Vehicle):
    def start(self) -> str:
        # override method
        parent_message = super().start()
        return f"{parent_message} (silently)"

    def fuel_type(self) -> str:
        return "Electric"


if __name__ == "__main__":
    v = Vehicle()
    e = ElectricCar()

    # Example 1: overridden method
    print(v.start())
    print(e.start())

    # Example 2: overridden fuel_type
    print("Vehicle fuel:", v.fuel_type())
    print("ElectricCar fuel:", e.fuel_type())
