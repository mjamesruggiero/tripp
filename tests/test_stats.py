#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import stats
import logging

logging.basicConfig(level=logging.ERROR, format="%(lineno)d\t%(message)s")


class TestStats(unittest.TestCase):

    def setUp(self):
        self.friends = [1, 3, 4, 5 ,2, 7, 5, 3, 13, 2, 9, 4]
        self.longer_sequence = [1, 2, 3, 4, 66, 77, 88, 10034]

    def test_mean(self):
        """stats -- mean"""
        result = stats.mean(self.friends)
        expected = 4.833333333333333
        self.assertEqual(expected, result)

    def test_median(self):
        """stats -- median"""
        result = stats.median(self.friends)
        self.assertEqual(4, result)

    def test_quantile(self):
        """stats -- quantile"""
        result = stats.quantile(self.friends, 0.10)
        self.assertEqual(2, result)

    def test_mode(self):
        """stats -- mode"""
        result = stats.mode(self.friends)
        self.assertEqual([2, 3, 4, 5], result)

    def test_data_range(self):
        """stats -- data range"""
        result = stats.data_range(self.longer_sequence)
        self.assertEqual(10033, result)

    def test_variance(self):
        """stats -- variance"""
        result = stats.variance(self.friends)
        self.assertEqual(10.64, round(result, 2))

    def test_standard_deviation(self):
        """stats -- standard deviation"""
        result = stats.standard_deviation(self.friends)
        self.assertEqual(3.26, round(result, 2))

    def test_interquartile_range(self):
        """stats -- interquartile_range"""
        result = stats.interquartile_range(self.friends)
        self.assertEqual(4, result)
