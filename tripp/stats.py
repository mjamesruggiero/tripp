# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
import algebra
import math
import logging

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def mean(x):
    """mean"""
    return sum(x) / len(x)


def median(v):
    """finds the middle-most value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2

    if n % 2 == 1:
        return sorted_v[midpoint]
    else:
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2


def quantile(x, p):
    """returns the p-th percentile value in x"""
    p_index = int(p * len(x))
    return sorted(x)[p_index]


def mode(x):
    """returns a list, might be mode > 1"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [i for i, count in counts.iteritems()
            if count == max_count]


def data_range(elements):
    """returns the difference
    between largest and smallest elements"""
    return max(elements) - min(elements)


def variance(elements):
    """assumes x has at least 2 elements"""
    n = len(elements)
    deviations = de_mean(elements)
    return algebra.sum_of_squares(deviations) / (n - 1)


def standard_deviation(x):
    return math.sqrt(variance(x))


def interquartile_range(elements):
    """the difference between
    the 75th percentile and 25th percentile"""
    return quantile(elements, 0.75) - quantile(elements, 0.25)


def de_mean(x):
    """translate x by subtracting the mean
    so that the result has mean zero"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


def covariance(x, y):
    """how variables vary in tandem from their means"""
    n = len(x)
    return algebra.dot(de_mean(x), de_mean(y)) / (n - 1)


def correlation(x, y):
    """divide the standard deviation of both variables"""
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0
