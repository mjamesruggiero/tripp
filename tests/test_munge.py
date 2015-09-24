#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import munge
import logging
import csv
import dateutil.parser
import datetime

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


class TestMunge(unittest.TestCase):
    def setUp(self):
        self.csv_file = "tests/fixtures/comma_delimited_stock_prices.csv"

    def test_parse_rows_with_utilizes_parsers(self):
        """munge - parse_rows_with"""
        data = []
        with open(self.csv_file, "rb") as f:
            reader = csv.reader(f)
            parsers = [dateutil.parser.parse, None, float]
            for line in munge.parse_rows_with(reader, parsers):
                data.append(line)

        expected_first_and_fourth = [
            [datetime.datetime(2014, 6, 20, 0, 0), 'AAPL', 90.91],
            [datetime.datetime(2014, 6, 19, 0, 0), 'MSFT', None]
        ]

        self.assertEqual(expected_first_and_fourth[0], data[0])
        self.assertEqual(expected_first_and_fourth[1], data[4])


    def test_parse_dict_utilized_parsers(self):
        """munge -- parse_dict"""
        test_dict = {
            "birthdate": "9/30/1967",
            "age": "29",
            "occupation": "Layabout",
            "zip": "94578"
        }
        parsers = {
            "birthdate": dateutil.parser.parse, "age": float, "zip": int
        }

        result = munge.parse_dict(test_dict, parsers)
        expected = {
            "birthdate": datetime.datetime(1967, 9, 30, 0, 0),
            "age": 29.0,
            "occupation": "Layabout",
            "zip": 94578
        }
        for k in expected:
            self.assertEqual(expected[k], result.get(k))
