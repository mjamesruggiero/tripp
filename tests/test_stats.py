#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import stats


class TestStats(unittest.TestCase):

    def setUp(self):
        self.friends = [1, 3, 4, 5 ,2, 7, 5, 3, 13, 2, 9, 4]

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
