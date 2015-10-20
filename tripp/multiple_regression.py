from algebra import dot
import gradient
import random
import regression


def predict(x_i, beta):
    """assumes that the first element of each x_i is 1"""
    return dot(x_i, beta)


def error(x_i, y_i, beta):
    return y_i - predict(x_i, beta)


def squared_error(x_i, y_i, beta):
    return error(x_i, y_i, beta) ** 2


def squared_error_gradient(x_i, y_i, beta):
    """the gradient (with respect to beta)
    corresponding to the ith squared error term"""
    return [-2 * x_ij * error(x_i, y_i, beta)
            for x_ij in x_i]


def estimate_beta(x, y):
    """Find the optimal beta using stochastic gradient descent"""
    beta_initial = [random.random() for x_i in x[0]]
    return gradient.minimize_stochastic(squared_error,
                                        squared_error_gradient,
                                        x,
                                        y,
                                        beta_initial,
                                        0.001)


def multiple_r_squared(x, y, beta):
    sum_of_squared_errors = sum(error(x_i, y_i, beta) ** 2
                                for x_i, y_i in zip(x, y))
    return 1.0 - sum_of_squared_errors / regression.total_sum_of_squares(y)
