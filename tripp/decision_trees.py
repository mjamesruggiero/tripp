from __future__ import division
from collections import Counter, defaultdict
from functools import partial
import math


def entropy(class_probabilities):
    """given a list of probabilities, compute the entropy"""
    return sum(-p * math.log(p, 2)
               for p in class_probabilities
               if p)   # test for zero


def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count for count in Counter(labels).values()]


def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)


def partition_entropy(subsets):
    """find the entropy from this partition of data into subsets"""
    total_count = sum(len(subset) for subset in subsets)

    return sum(data_entropy(subset) * len(subset) / total_count
               for subset in subsets)


def group_by(items, key_fn):
    """retuns a defaultdict(list) where each input item
    is in the list whose key is key_fn(item)"""
    groups = defaultdict(list)
    for item in items:
        key = key_fn(item)
        groups[key].append(item)
    return groups


def partition_by(inputs, attribute):
    """retuns a dict of inputs partitioned by the attribute;
    each in put is a pair (attribute_dict, label)"""
    return group_by(inputs, lambda x: x[0][attribute])


def partition_entropy_by(inputs, attribute):
    """computes the entropy corresponding to the given partition """
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())


def classify(tree, input):
    """classify the input using the given decision tree"""

    # if this is a leaf, return it
    if tree in [True, False]:
        return tree

    # find correct subtree
    attribute, subtree_dict = tree

    subtree_key = input.get(attribute)

    if subtree_key not in subtree_dict:
        subtree_key = None

    subtree = subtree_dict[subtree_key]
    return classify(subtree, input)


def build_tree_id3(inputs, split_candidates=None):
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()

    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label])
    num_falses = num_inputs - num_trues

    if num_trues == 0:
        return False
    if num_falses == 0:
        return True

    if not split_candidates:
        return num_trues >= num_falses

    best_attribute = min(split_candidates,
                         key=partial(partition_entropy_by, inputs))

    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates if a != best_attribute]

    # recursively build the subtrees
    subtrees = {attribute: build_tree_id3(subset, new_candidates)
                for attribute, subset in partitions.iteritems()}

    subtrees[None] = num_trues > num_falses   # default case

    return (best_attribute, subtrees)


def forest_classify(trees, input):
    votes = [classify(tree, input) for tree in trees]
    vote_counts = Counter(votes)
    return vote_counts.most_common(1)[0][0]
