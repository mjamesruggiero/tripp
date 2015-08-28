# -*- coding: utf-8 -*-
from __future__ import division
from collections import Counter
from algebra import sum_of_squares
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
    n = mean(elements)
    dev2 = [(x - n)**2 for x in elements]
    return mean(dev2)

def standard_deviation(x):
    return math.sqrt(variance(x))

def interquartile_range(elements):
    """the difference between
    the 75th percentile and 25th percentile"""
    return quantile(elements, 0.75) - quantile(elements, 0.25)
