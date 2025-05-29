from __future__ import annotations

from cmath import exp, pi

from vector_utils import dot
from matrix_utils import matrix_times_vector

from other_utils import abs_square


def roots_of_unity_k_n(k: complex, n: complex) -> list(complex):
    return [exp(2j * pi * (k * m % n) / n) for m in range(n)]


def dft_k(x, k):
    return dot(x, roots_of_unity_k_n(k, len(x)))


def psd_k(x, k):
    x_hat_k = dft_k(x, k)
    return abs_square(x_hat_k)


def dft_matrix(n):
    w_n = roots_of_unity_k_n(1, n)
    return [[w_n[(j * k) % n] for j in range(n)] for k in range(n)]


def dft(x):
    transform_matrix = dft_matrix(len(x))
    return matrix_times_vector(transform_matrix, x)


def psd(x):
    x_hat = dft(x)
    return [abs_square(x_hat_i) for x_hat_i in x_hat]


def main():  # pragma: no cover
    print("Entry point for playing around")


if __name__ == "__main__":  # pragma: no cover
    main()
