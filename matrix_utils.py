from vector_utils import dot


def transpose(matrix):
    return [list(col) for col in zip(*matrix)]


def matrix_mul(a, b):
    return [[dot(a_i, b_t_j) for a_i in a] for b_t_j in transpose(b)]


def matrix_times_vector(a, x):
    return [dot(a_i, x) for a_i in a]


def main():  # pragma: no cover
    print("Entry point for playing around")


if __name__ == "__main__":  # pragma: no cover
    main()
