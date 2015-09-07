#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import unittest

from tripp import probability


logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


class TestProbability(unittest.TestCase):

    def setUp(self):
        self.xs = [x / 10.0 for x in range(-10, 10)]

    def test_uniform_pdf_greater_or_equal_t0_zero(self):
        """probability -- uniform_pdf greater than or equal to 0"""
        self.assertEqual(1, probability.uniform_pdf(0.4))

    def test_uniform_pdf_equal_to_zero(self):
        """probability -- uniform_pdf equal to zero"""
        self.assertEqual(1, probability.uniform_pdf(0.0))

    def test_uniform_pdf_greater_than_one(self):
        """probability -- uniform pdf greater than 1"""
        self.assertEqual(0, probability.uniform_pdf(3))

    def test_uniform_cdf_greater_or_equal_t0_zero(self):
        """probability -- uniform_cdf greater than or equal to 0"""
        self.assertEqual(0.4, probability.uniform_cdf(0.4))

    def test_uniform_cdf_equal_to_zero(self):
        """probability -- uniform_cdf equal to zero"""
        self.assertEqual(0, probability.uniform_cdf(-4))

    def test_uniform_cdf_greater_than_one(self):
        """probability -- uniform cdf greater than 1"""
        self.assertEqual(1, probability.uniform_cdf(3))

    def test_normal_pdf_with_sigma_1(self):
        """probability -- normal pdf with sigma of 1"""
        result = [probability.normal_pdf(x, sigma=1) for x in self.xs]
        expected = [0.24197072451914337,
                    0.2660852498987548,
                    0.28969155276148273,
                    0.31225393336676127,
                    0.33322460289179967,
                    0.3520653267642995,
                    0.36827014030332333,
                    0.38138781546052414,
                    0.3910426939754559,
                    0.3969525474770118,
                    0.3989422804014327,
                    0.3969525474770118,
                    0.3910426939754559,
                    0.38138781546052414,
                    0.36827014030332333,
                    0.3520653267642995,
                    0.33322460289179967,
                    0.31225393336676127,
                    0.28969155276148273,
                    0.2660852498987548]
        self.assertEqual(expected, result)

    def test_normal_pdf_with_sigma_zero_point_five(self):
        """probability -- normal pdf with sigma of 0.5"""
        result = [probability.normal_pdf(x, sigma=0.5) for x in self.xs]
        expected = [0.10798193302637613,
                    0.1579003166017883,
                    0.2218416693589111,
                    0.29945493127148975,
                    0.38837210996642596,
                    0.48394144903828673,
                    0.5793831055229655,
                    0.6664492057835993,
                    0.7365402806066467,
                    0.7820853879509118,
                    0.7978845608028654,
                    0.7820853879509118,
                    0.7365402806066467,
                    0.6664492057835993,
                    0.5793831055229655,
                    0.48394144903828673,
                    0.38837210996642596,
                    0.29945493127148975,
                    0.2218416693589111,
                    0.1579003166017883]
        self.assertEqual(expected, result)

    def test_inverse_normal_cdf(self):
        """probability -- inverse normal cdf"""
        # test case taken from http://bit.ly/1hAdejH
        p_values = [0.0000001,
                    0.00001,
                    0.001,
                    0.05,
                    0.15,
                    0.25,
                    0.35,
                    0.45,
                    0.55,
                    0.65,
                    0.75,
                    0.85,
                    0.95,
                    0.999,
                    0.99999,
                    0.9999999]
        expected_inverse_normals = [-5.199337582187471,
                                    -4.264890793922602,
                                    -3.090232306167813,
                                    -1.6448536269514729,
                                    -1.0364333894937896,
                                    -0.6744897501960817,
                                    -0.38532046640756773,
                                    -0.12566134685507402,
                                    0.12566134685507402,
                                    0.38532046640756773,
                                    0.6744897501960817,
                                    1.0364333894937896,
                                    1.6448536269514729,
                                    3.090232306167813,
                                    4.264890793922602,
                                    5.199337582187471]
        for i, p in enumerate(p_values):
            significant_digit = 3
            result = round(probability.inverse_normal_cdf(p), significant_digit)
            expected = round(expected_inverse_normals[i], significant_digit)
            self.assertEqual(result, expected)
