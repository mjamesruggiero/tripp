import csv
import sys
import logging
import random
import decision_trees
import argparse

logging.basicConfig(level=logging.DEBUG, format="%(lineno)d\t%(message)s")

# grab CSV of rates
# decorate with features (in this case, "action" and "brand")
# create tuples that indicate ads w/ CTRS greater than x
# partition entropy


def csv_data(filepath, new_parent_key='creative_key'):
    _dict = {}
    with open(filepath) as _csv:
        reader = csv.DictReader(_csv)
        for row in reader:
            _dict[row[new_parent_key]] = row
    return _dict


def combine_csvs(rates_file, creatives_file):
    rates = csv_data(rates_file, 'creative_key')
    creatives = csv_data(creatives_file, 'key')

    rates_i_cant_decorate = []
    for key in rates:
        if key in creatives:
            rates[key]['action'] = creatives[key]['action']
            rates[key]['brand'] = creatives[key]['brand']
        else:
            rates_i_cant_decorate.append(key)

    for k in rates_i_cant_decorate:
        del rates[k]
    return rates


def build_tree(rates, minimum=0.7):
    tuples = []
    for key in rates:
        number = rates[key]['rate']
        rates[key]['rate'] = float(number)
        is_enough = False
        if rates[key]['rate'] >= minimum:
            logging.info("true for {}".format(rates[key]))
            is_enough = True
        tup = (rates[key], is_enough)
        tuples.append(tup)

    return tuples


def main(rates_file, creatives_file):
    combined = combine_csvs(rates_file, creatives_file)

    rates_tree = build_tree(combined)

    logging.info("rates_tree looks like {}".format(random.choice(rates_tree)))

    keys = ['action', 'creative_key', 'brand']
    ranks = partition(rates_tree, keys)
    return ranks


def partition(rates_data, keys):
    partitioned = [[key,
                    decision_trees.partition_entropy_by(rates_data, key)]
                   for key in keys]

    return sorted(partitioned, key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    DESCRIPTION = 'Builds random forest for optimizing ad clickthrough'
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('rates_file', action="store")
    parser.add_argument('creatives_file', action="store")

    results = parser.parse_args()
    rates_file = results.rates_file
    creatives_file = results.creatives_file

    result = main(rates_file, creatives_file)

    logging.info("ranks is {}".format(result))
