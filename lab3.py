import numpy as np
import time

class GaloisField:
    def __init__(self, m, irreducible_poly):
        self.m = m
        self.poly = irreducible_poly
        self.field_size = 2 ** m

    def add(self, a, b):
        return a ^ b

    def multiply(self, a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & self.field_size:
                a ^= self.poly_as_int()
        return result

    def poly_as_int(self):
        terms = self.poly.split(" + ")
        result = 0
        for term in terms:
            if term == "1":
                result ^= 1
            elif term.startswith("x"):
                if "^" in term:
                    power = int(term.split("^")[1])
                    result ^= 1 << power
                else:
                    result ^= 1 << 1
        return result

    def trace(self, a):
        result = a
        for _ in range(1, self.m):
            a = self.square(a)
            result ^= a
        return result

    def square(self, a):
        return self.multiply(a, a)

    def power(self, a, exp):
        result = 1
        while exp:
            if exp & 1:
                result = self.multiply(result, a)
            a = self.square(a)
            exp >>= 1
        return result

    def inverse(self, a):
        return self.power(a, self.field_size - 2)

    def to_binary(self, a):
        return bin(a)[2:].zfill(self.m)

    def from_binary(self, binary):
        return int(binary, 2)

def test_field_operations():
    m = 409
    irreducible_poly = "x^409 + x^15 + x^6 + x + 1"
    gf = GaloisField(m, irreducible_poly)

    # Константи
    zero = 0
    one = 1
    print("Нуль (нейтральний елемент для додавання):", zero)
    print("Одиниця (нейтральний елемент для множення):", one)

    # Додавання
    a = 12345
    b = 67890
    print(f"Додавання {a} + {b} = {gf.add(a, b)}")

    # Множення
    c = 54321
    print(f"Множення {b} * {c} = {gf.multiply(b, c)}")

    # Слід елемента
    trace_a = gf.trace(a)
    print(f"Слід елемента {a} = {trace_a}")

    # Зведення у квадрат
    square_a = gf.square(a)
    print(f"Квадрат елемента {a} = {square_a}")

    # Зведення у довільний степінь
    power = 57
    pow_a = gf.power(a, power)
    print(f"Елемент {a} у степені {power} = {pow_a}")

    # Обернений елемент
    inverse_a = gf.inverse(a)
    print(f"Множення оберненого елемента {a} = {inverse_a}")

    # Перетворення у бінарний рядок і назад
    binary_a = gf.to_binary(a)
    print(f"Бінарне представлення елемента {a} = {binary_a}")

    from_binary = gf.from_binary(binary_a)
    print(f"Елемент із бінарного рядка {binary_a} = {from_binary}")

def measure_performance():
    m = 409
    irreducible_poly = "x^409 + x^15 + x^6 + x + 1"
    gf = GaloisField(m, irreducible_poly)

    a = 12345
    b = 67890

    # Вимірювання додавання
    start = time.time()
    for _ in range(1000):
        _ = gf.add(a, b)
    add_time = (time.time() - start) / 1000

    # Вимірювання множення
    start = time.time()
    for _ in range(1000):
        _ = gf.multiply(a, b)
    mul_time = (time.time() - start) / 1000

    # Вимірювання обчислення сліду
    start = time.time()
    for _ in range(1000):
        _ = gf.trace(a)
    trace_time = (time.time() - start) / 1000

    print("Середній час виконання (у секундах):")
    print(f"Додавання: {add_time:.6f}s")
    print(f"Множення: {mul_time:.6f}s")
    print(f"Обчислення сліду: {trace_time:.6f}s")

def main():
    test_field_operations()
    measure_performance()

if __name__ == "__main__":
    main()
