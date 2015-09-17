#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import gradient
from tripp import algebra
from functools import partial
import random
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

    def test_step(self):
        """gradient -- step"""
        v = [random.randint(-10, 10) for i in range(3)]

        tolerance = 0.0000001
        while True:
            _gradient = gradient.sum_of_squares_gradient(v)
            next_v = gradient.step(v, _gradient, -0.01)
            if algebra.distance(next_v, v) < tolerance:
                break
            v = next_v

        expected = [0.0, 0.0, 0.0]
        returned = map(lambda x: round(x, 5), v)
        self.assertEqual(returned, expected)

    def test_negate(self):
        """gradient -- negate"""
        vals = [2, 4.5, 99, 0.000005]
        funcs = [
            lambda w: 7 * w + 5,
            lambda x: x * 2,
            lambda y: y ** 4,
            lambda z: 2 * z - 7,
            lambda w: 7 * w + 5]
        for v, f in zip(vals, funcs):
            result = f(v)
            negation = gradient.negate(f)
            self.assertEqual(result * -1, negation(v))
