#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import decision_trees


class TestDecisionTrees(unittest.TestCase):

    def setUp(self):
        self.inputs = [
            ({'level': 'Senior',
              'lang': 'Java',
              'tweets': 'no',
              'phd': 'no'}, False),
            ({'level': 'Senior',
              'lang': 'Java',
              'tweets': 'no',
              'phd': 'yes'}, False),
            ({'level': 'Mid',
              'lang': 'Python',
              'tweets': 'no',
              'phd': 'no'}, True),
            ({'level': 'Junior',
              'lang': 'Python',
              'tweets': 'no',
              'phd': 'no'}, True),
            ({'level': 'Junior',
              'lang': 'R',
              'tweets': 'yes',
              'phd': 'no'}, True),
            ({'level': 'Junior',
              'lang': 'R',
              'tweets': 'yes',
              'phd': 'yes'}, False),
            ({'level': 'Mid',
              'lang': 'R',
              'tweets': 'yes',
              'phd': 'yes'}, True),
            ({'level': 'Senior',
              'lang': 'Python',
              'tweets': 'no',
              'phd': 'no'}, False),
            ({'level': 'Senior',
              'lang': 'R',
              'tweets': 'yes',
              'phd': 'no'}, True),
            ({'level': 'Junior',
              'lang': 'Python',
              'tweets': 'yes',
              'phd': 'no'}, True),
            ({'level': 'Senior',
              'lang': 'Python',
              'tweets': 'yes',
              'phd': 'yes'}, True),
            ({'level': 'Mid',
              'lang': 'Python',
              'tweets': 'no',
              'phd': 'yes'}, True),
            ({'level': 'Mid',
              'lang': 'Java',
              'tweets': 'yes',
              'phd': 'no'}, True),
            ({'level': 'Junior',
              'lang': 'Python',
              'tweets': 'no',
              'phd': 'yes'},
             False)
        ]

    def test_partition_entropy_by(self):
        """decision_trees -- partition_entropy_by"""
        keys = ['level', 'lang', 'tweets', 'phd']
        partitioned = [[key,
                        decision_trees.partition_entropy_by(self.inputs, key)]
                       for key in keys]

        ranked = sorted(partitioned, key=lambda x: x[1], reverse=True)
        first_rank = ranked[0][0]
        self.assertEqual('phd', first_rank)
