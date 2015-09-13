#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import gradient
from functools import partial
import logging

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def square(x):
    """for testing"""
    return x * x


def derivative(x):
    """for testing"""
    return 2 * x


class TestGradient(unittest.TestCase):

    def setUp(self):
        pass

    def test_sum_of_squares(self):
        """gradient -- sum of squares"""
        sut = [1, 2, 3, 4, 5]
        result = gradient.sum_of_squares(sut)
        self.assertEqual(result, 55)

    def test_derivative_estimates(self):
        """gradient -- difference quotient"""
        derivative_estimate = partial(gradient.difference_quotient,
                                      square,
                                      h=0.00001)
        x = range(-10, 10)
        actuals = map(derivative, x)
        estimates = map(derivative_estimate, x)
        for comparison in zip(actuals, estimates):
            actual, estimate = comparison
            self.assertEqual(actual, int(round(estimate, 1)))
