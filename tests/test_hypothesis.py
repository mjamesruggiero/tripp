#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import random
from .context import tripp
from tripp import hypothesis
import logging


logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


class TestHypothesis(unittest.TestCase):

    def test_normal_approximation_to_binomial(self):
        """hypothesis -- normal_approximation_to_binomial"""
        n = 1000
        p = 0.5
        expected_mu = 500.0
        expected_sigma = 15.8114
        mu, sigma = hypothesis.normal_approximation_to_binomial(n, p)
        self.assertEqual(mu, expected_mu)
        self.assertEqual(round(sigma, 4), expected_sigma)

    def test_p_hacking(self):
        """hypothesis -- run_experiment"""
        random.seed(0)
        experiments = [hypothesis.run_experiment() for _ in range(1000)]
        num_rejections = len([x for x in experiments
                             if hypothesis.reject_fairness(x)])
        logging.debug("num_rejections is {}".format(num_rejections))
        self.assertEqual(num_rejections, 46)

    def test_a_b_test_statistic(self):
        """hypothesis -- a_b_test_statistic"""
        result = hypothesis.a_b_test_statistic(1000, 200, 1000, 180)
        self.assertEqual(round(result, 2), -1.14)
