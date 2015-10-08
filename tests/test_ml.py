#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import ml


class TestMl(unittest.TestCase):

    def setUp(self):
        self.true_pos = 70.0
        self.false_pos = 4930.0
        self.false_neg = 13930.0
        self.true_neg = 981070.0

    def test_accuracy(self):
        """ml -- accuracy"""
        acc = ml.accuracy(self.true_pos,
                          self.false_pos,
                          self.false_neg,
                          self.true_neg)
        self.assertEqual(0.98114, acc)

    def test_precision(self):
        """ml -- precision"""
        prec = ml.precision(self.true_pos,
                            self.false_pos,
                            self.false_neg,
                            self.true_neg)
        self.assertEqual(0.014, prec)

    def test_recall(self):
        """ml -- recall"""
        rec = ml.recall(self.true_pos,
                        self.false_pos,
                        self.false_neg,
                        self.true_neg)
        self.assertEqual(0.005, rec)

    def test_f1_score(self):
        """ml -- f1_score"""
        f1 = ml.f1_score(self.true_pos,
                         self.false_pos,
                         self.false_neg,
                         self.true_neg)
        self.assertEqual(0.00736842105263158, f1)
