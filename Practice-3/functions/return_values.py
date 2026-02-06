def divide(a: float, b: float):
    if b == 0:
        return None
    return a / b
print(divide(10, 0))

def add(a,b):
    return a+b
print(add(10,30))

def total_price(prices: list[float]) -> float:
    return sum(prices)

def is_even(n: int) -> bool:
    return n % 2 == 0
print(is_even(1))

def find_first_even(numbers: list[int]) -> int | None:
    # Return the first even number, or None if not found
    for n in numbers:
        if n % 2 == 0:
            return n
    return None