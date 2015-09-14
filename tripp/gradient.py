import logging

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def sum_of_squares(v):
    """computes the sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)


def difference_quotient(f, x, h):
    """the limit of the difference quotients"""
    return (f(x + h) - f(x)) / h


def step(v, direction, step_size):
    """move step_size in the direction from v"""
    return [v_i + step_size * direction_i
            for v_i, direction_i in zip(v, direction)]


def sum_of_squares_gradient(v):
    return [2 * i for i in v]
