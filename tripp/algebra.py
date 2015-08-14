# -*- coding: utf-8 -*-
import math
import logging

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def vector_add(v, w):
    """adds corresponding vectors"""
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def vector_subtract(v, w):
    """subtracts corresponding elements"""
    return [v_i - w_i for v_i, w_i in zip(v, w)]


def vector_sum(vectors):
    """sums all corresponding elements"""
    return reduce(vector_add, vectors)


def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]


def vector_mean(vectors):
    """compute the vector whose ith element is
    the mean of the ith elements of the input vectors"""
    n = len(vectors)
    logging.debug("length is {0}, scalar is {1}"
                  .format(n, 1/float(n)))
    return scalar_multiply(1/float(n), vector_sum(vectors))


def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)


def magnitude(v):
    return math.sqrt(sum_of_squares(v))


def squared_distance(v, w):
    """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_subtract(v, w))


def distance(v, w):
    """the distance between two vectors"""
    return math.sqrt(squared_distance(v, w))
