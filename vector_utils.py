def dot(x, y):
    return sum([x_i * y_i for x_i, y_i in zip(x, y)])


def rotate_left(x):
    return x[1:] + [x[0]]


def rotate_right(x):
    return [x[-1]] + x[:-1]


def rotate_n(x, n):
    l = len(x)
    return [x[(i + n) % l] for i in range(l)]


def reverse(x):
    return x[-1:0:-1] + [x[0]]


def pad_right(x, n):
    return x + ([0] * n)


def pad_left(x, n):
    return ([0] * n) + x


def pointwise_operation(op, *x):
    return [op(*x_i) for x_i in zip(*x)]


def convolution(x, y):
    x_padded = pad_left(x, len(y) - 1)
    y_reverse_padded = pad_right(reverse(y), len(x) - 1)
    length = len(x) + len(y) - 1
    return [dot(x_padded, rotate_n(y_reverse_padded, -k)) for k in range(length)]


def correlation(x, y):
    return convolution(x, reverse(y))


def circular_convolution(x, y):
    assert len(x) == len(y)
    y_reverse = reverse(y)
    return [dot(x, rotate_n(y_reverse, -k)) for k in range(len(x))]


def circular_correlation(x, y):
    return [dot(x, rotate_n(y, k)) for k in range(len(x))]


def distance_l2(x, y):
    norm_square = lambda x_i, y_i: abs(x_i - y_i) * abs(x_i - y_i)
    return sum(pointwise_operation(norm_square, x, y))


def main():  # pragma: no cover
    print("Entry point for playing around")


if __name__ == "__main__":  # pragma: no cover
    main()
