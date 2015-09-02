# -*- coding: utf-8 -*-
import logging
import math

logging.basicConfig(level=logging.ERROR, format="%(lineno)d\t%(message)s")


def uniform_pdf(x):
    return 1 if x >= 0 and x < 1 else 0


def uniform_cdf(x):
    """returns the probability that
    a uniform random variable is <= x"""
    if x < 0:
        return 0
    elif x < 1:
        return x
    else:
        return 1


def normal_pdf(x, mu=0, sigma=1):
    """classic bell-shaped distribution"""
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-(x - mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))
