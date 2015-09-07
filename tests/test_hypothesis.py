#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import hypothesis
import logging


logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


class TestHypothesis(unittest.TestCase):

    def setUp(self):
        pass

    def test_normal_approximation_to_binomial(self):
        """hypothesis -- normal_approximation_to_binomial"""
        n = 1000
        p = 0.5
        expected_mu = 500.0
        expected_sigma = 15.8114
        mu, sigma = hypothesis.normal_approximation_to_binomial(n, p)
        self.assertEqual(mu, expected_mu)
        self.assertEqual(round(sigma, 4), expected_sigma)
