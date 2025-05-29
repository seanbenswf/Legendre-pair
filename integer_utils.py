from __future__ import annotations


def primes():
    yield 2
    yield 3

    increment_value = [2, 4]

    current_value = 5
    crossed_numbers = dict()

    for increment in cycle(increment_value):
        if current_value in crossed_numbers:
            step = crossed_numbers[current_value]
            next = current_value + step
            while next in crossed_numbers:
                next += step
            crossed_numbers[next] = step
            del crossed_numbers[current_value]
        else:
            crossed_numbers[current_value * current_value] = 6 * current_value
            crossed_numbers[current_value * (current_value + increment)] = (
                6 * current_value
            )
            yield current_value

        current_value += increment


def cycle(numbers):
    while True:
        for num in numbers:
            yield num


def gcd_extended(a: int, b: int) -> tuple(int, int, int):

    # Base Case
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcd_extended(b % a, a)

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def gcd(a: int, b: int) -> int:
    g, _, _ = gcd_extended(a, b)
    return g


def primorial(n: int) -> int:
    prime_generator = primes()
    pr = 1
    for _ in range(n):
        pr *= next(prime_generator)

    return pr


def relative_primes(n: int):
    return [m for m in range(1, n) if gcd(n, m) == 1]


def order_of(number: int, field_size: int) -> int:

    if gcd(number, field_size) != 1:
        return 0

    order = 1
    current = number % field_size
    while current != 1:
        order += 1
        current *= number
        current %= field_size

    return order


def prime_factorization(n: int):
    factors = dict()
    if n <= 1:
        return factors
    for possible_factors in primes():
        while n % possible_factors == 0:
            factors[possible_factors] = factors.get(possible_factors, 0) + 1
            n //= possible_factors
        if n == 1:
            break

    return factors


def totient(n: int) -> int:
    factors = prime_factorization(n)

    t = 1
    for factor, power in factors.items():
        a = factor ** (power - 1)
        t *= a * factor - a

    return t


def jacobi(a: int, n: int):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0


def main():  # pragma: no cover
    print("Entry point for playing around")


if __name__ == "__main__":  # pragma: no cover
    main()
