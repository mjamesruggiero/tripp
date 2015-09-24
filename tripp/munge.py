from bs4 import BeautifulSoup
from collections import Counter
from time import sleep
import math
import matplotlib.pyplot as pyplot
import probability
import re
import requests
import random
import json
import algebra
import stats


def bucketize(point, bucket_size):
    """floor the point to the next lower multiple of bucket size"""
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)


def plot_histogram(points, bucket_size, title="", asset="histogram.png"):
    """generate plot for bucketed data"""
    histogram = make_histogram(points, bucket_size)
    pyplot.bar(histogram.keys(), histogram.values(), width=bucket_size)
    pyplot.title(title)
    pyplot.savefig(asset)


def random_normal():
    """returns a random draw from a standard normal distribution"""
    return probability.inverse_normal_cdf(random.random())


def correlation_matrix(data):
    """returns the num_columns x num_columns matrix whose (i, j)th entry
    is the correlation between columns i and j of data"""
    _, num_columns = algebra.shape(data)

    def matrix_entry(i, j):
        return stats.correlation(algebra.get_column(data, i),
                                 algebra.get_column(data, j))

    return algebra.mk_matrix(num_columns, num_columns, matrix_entry)


def make_random_matrix():
    _points = 100

    def random_row():
        row = [None, None, None, None]
        row[0] = random_normal()
        row[1] = -5 * row[0] + random_normal()
        row[2] = row[0] + row[1] + 5 * random_normal()
        row[3] = 6 if row[2] > -2 else 0
        return row

    random.seed(0)
    data = [random_row() for _ in range(_points)]
    return data


def parse_row(input_row, parsers):
    """Given a list of parsers (whose values can be None)
    apply the appropriate one to eac element of input_row"""
    return [parse_or_mk_none(parser)(value)
            if parser is not None else value
            for value, parser in zip(input_row, parsers)]


def parse_rows_with(reader, parsers):
    """Wrap a reader to apply the parsers to each of its rows"""
    for row in reader:
        yield parse_row(row, parsers)


def parse_or_mk_none(f):
    """Wrap f to return None if f raises;
    assumes f takes 1 input)"""
    def f_or_none(x):
        try:
            return f(x)
        except:
            return None
    return f_or_none


def try_parse_field(field_name, value, parser_dict):
    """try to parse value using the appropriate function from parser dict"""
    parser = parser_dict.get(field_name)
    if parser is not None:
        return parse_or_mk_none(parser)(value)
    else:
        return value

def parse_dict(input_dict, parsers):
    return { field_name: try_parse_field(field_name, value, parsers)
            for field_name, value in input_dict.iteritems() }


if __name__ == '__main__':
    test = 'MATRIX'

    if test == 'HISTOGRAM':
        random.seed(0)
        uniform = [200 * random.random() - 100 for _ in range(10000)]
        normal = [57 * probability.inverse_normal_cdf(random.random())
                  for _ in range(10000)]

        plot_histogram(uniform, 10, 'Uniform Histogram', 'uniform.png')
        plot_histogram(normal, 10, 'Normal Histogram', 'normal.png')


    if test == 'SCATTER':
        asset = 'scatter.png'
        xs = [random_normal() for _ in range(1000)]
        ys1 = [x + random_normal() / 2 for x in xs]
        ys2 = [-x + random_normal() / 2 for x in xs]

        pyplot.scatter(xs, ys1, marker='.', color='black', label='ys1')
        pyplot.scatter(xs, ys2, marker='.', color='gray', label='ys2')
        pyplot.xlabel('xs')
        pyplot.ylabel('ys')
        pyplot.legend(loc=9)
        pyplot.savefig(asset)

        # look at the correlations
        print "correlation of xs and ys1: {}".format(stats.correlation(xs, ys1))
        print "correlation of xs and ys2: {}".format(stats.correlation(xs, ys2))

    if test == 'MATRIX':
        c_matrix = correlation_matrix(make_random_matrix())
        print "correlation matrix of random matrix: {}".format(c_matrix)
