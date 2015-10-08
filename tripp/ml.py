import random


def split_data(data, prob):
    """split data into fractions [prob, 1 - prob]"""
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results


def train_test_split(x, y, test_percent):
    """pair corresponding values in split groups
    through magical un-zipping tricks"""
    data = zip(x, y)
    train, test = split_data(data, 1 - test_percent)
    x_train, y_train = zip(*train)
    x_test, y_test = zip(*test)
    return x_train, x_test, y_train, y_test


def accuracy(tp, fp, fn, tn):
    correct = tp + tn
    total = tp + fp + fn + tn
    return correct / total


def precision(tp, fp, fn, tn):
    """how accurate is your prediction?"""
    return tp / (tp + fp)


def recall(tp, fp, fn, tn):
    """what fraction of the positives did the model identify?"""
    return tp / (tp + fn)


def f1_score(tp, fp, fn, tn):
    """the harmonic mean of precision and recall"""
    p = precision(tp, fp, fn, tn)
    r = recall(tp, fp, fn, tn)
    return 2 * p * r / (p + r)
