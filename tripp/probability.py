# -*- coding: utf-8 -*-
import logging
import math
import random

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


def normal_cdf(x, mu=0, sigma=1):
    """the probability that a real-valued random variable X
    with a given probability distribution will be found
    to have a value less than or equal to x"""
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find approximate inverse using binary search"""
    # if not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu * sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z = -10.0  # normal_cdf(-10) is very close to 0
    hi_z = 10.0   # normal_cdf(10) is very close to 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2  # find the midpoint
        mid_p = normal_cdf(mid_z)   # and its corresponding cdf
        if mid_p < p:
            # midpoint still too low, search above
            low_z = mid_z
        elif mid_p > p:
            # midpoint too high, search below
            hi_z = mid_z
        else:
            break
    return mid_z


def bernoulli_trial(p):
    return 1 if random.random() < p else 0


def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))
