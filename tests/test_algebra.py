#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .context import tripp
from tripp import algebra


class TestAlgebra(unittest.TestCase):

    def setUp(self):
        self.a = [63.0, 150.0]
        self.b = [67.0, 160.0]
        self.c = [100.0, 100.0]

    def test_vector_add(self):
        """algebra -- vector addition"""
        added = algebra.vector_add(self.a, self.b)
        self.assertEqual([130, 310], added)

    def test_vector_subtract(self):
        """algebra -- vector subraction"""
        subtracted = algebra.vector_subtract(self.a, self.b)
        self.assertEqual([-4, -10], subtracted)

    def test_vector_sum(self):
        """algebra -- vector sum"""
        summed = algebra.vector_sum([self.c, self.a, self.b])
        self.assertEqual([230, 410], summed)

    def test_vector_multiply(self):
        """algebra -- vector multiplication"""
        scalar = 9
        multiplied = algebra.scalar_multiply(scalar, self.c)
        self.assertEqual([900, 900], multiplied)

    def test_vector_mean(self):
        """algebra -- vector mean"""
        vecs = [self.a, self.b, self.c]
        mean = algebra.vector_mean(vecs)
        expected = [76.66666666666666, 136.66666666666666]
        self.assertEqual(expected, mean)

    def test_dot(self):
        """algebra -- dot"""
        _dot = algebra.dot(self.a, self.b)
        self.assertEqual(28221.0, _dot)

    def test_sum_of_squares(self):
        """algebra -- sum of squares"""
        _sum_of_squares = algebra.sum_of_squares(self.a)
        self.assertEqual(26469.0, _sum_of_squares)

    def test_magnitude(self):
        """algebra -- magnitude"""
        _magnitude = algebra.magnitude(self.a)
        self.assertEqual(162.69296235547498, _magnitude)

    def test_squared_distance(self):
        """algebra -- squared distance"""
        _sq_dist = algebra.squared_distance(self.a, self.b)
        self.assertEqual(116.0, _sq_dist)

    def test_distance(self):
        """algebra -- distance"""
        dist = algebra.distance(self.a, self.b)
        self.assertEqual(10.77, round(dist, 2))
