from bs4 import BeautifulSoup
from collections import Counter, defaultdict
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


def picker(field_name):
    """returns function that picks a field out of a dict"""
    return lambda row: row[field_name]


def pluck(field_name, rows):
    """turns list of dicts into list of field_name values"""
    return map(picker(field_name), rows)


def group_by(grouper, rows, value_transform=None):
    """key is output of grouper, value is list of rows"""
    grouped = defaultdict(list)
    for row in rows:
        grouped[grouper(row)].append(row)
    if value_transform is None:
        return grouped
    else:
        return { key: value_transform(rows)
                 for key, rows in grouped.iteritems() }

def scale(data_matrix):
    """returns the mean and standard deviations of each column"""
    num_rows, num_cols = algebra.shape(data_matrix)
    means = [stats.mean(algebra.get_column(data_matrix, j))
             for j in range(num_cols)]

    stddevs = [stats.standard_deviation(algebra.get_column(data_matrix, j))
                                  for j in range(num_cols)]
    return means, stddevs

def rescale(data_matrix):
    """rescales the input data so that each column
    has mean 0 and StdDev 1;
    leaves alone columns with no deviation"""
    means, stddevs = scale(data_matrix)

    def rescaled(i, j):
        if stddevs[j] > 0:
            return (data_matrix[i][j] - means[j]) /  stddevs[j]
        else:
            return data_matrix[i][j]

    num_rows, num_cols = algebra.shape(data_matrix)
    return algebra.mk_matrix(num_rows, num_cols, rescaled)
