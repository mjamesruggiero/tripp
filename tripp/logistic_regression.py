import math
import algebra


def logistic(x):
    return 1.0 / (1 + math.exp(-x))


def logistic_prime(x):
    return logistic(x) * (1 - logistic(x))


def logistic_log_likelihood_i(x_i, y_i, beta):
    if y_i == 1:
        return math.log(logistic(algebra.dot(x_i, beta)))
    else:
        return math.log(1 - logistic(algebra.dot(x_i, beta)))


def logistic_log_likelihood(x, y, beta):
    return sum(logistic_log_likelihood_i(x_i, y_i, beta)
               for x_i, y_i in zip(x, y))


def logistic_log_partial_ij(x_i, y_i, beta, j):
    """i is the index of the data point, j is the index
    of the derivative"""
    return (y_i - logistic(algebra.dot(x_i, beta))) * x_i[j]


def logistic_log_gradient_i(x_i, y_i, beta):
    """the gradient of the log likelihood
    corresponding to the ith data point"""
    return [logistic_log_partial_ij(x_i, y_i, beta, j)
            for j, _ in enumerate(beta)]


def logistic_log_gradient(x, y, beta):
    return reduce(algebra.vector_add,
                  [logistic_log_gradient_i(x_i, y_i, beta)
                   for x_i, y_i in zip(x, y)])
