from algebra import dot
import algebra
import gradient
import probability
import random
import regression
from functools import partial


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


def bootstrap_sample(data):
    """randomly sample len(data) elements with replacement"""
    return [random.choice(data) for _ in data]


def bootstrap_statistic(data, stats_fn, num_samples):
    """evaluates stats_fn on num_samples bootstrap samples from data"""
    return [stats_fn(bootstrap_sample(data)) for _ in range(num_samples)]


def estimate_sample_beta(sample):
    """sample is a list of pairs (x_i, y_i)"""
    x_sample, y_sample = zip(*sample)  # magic unzipping trick
    return estimate_beta(x_sample, y_sample)


def p_value(beta_hat_j, sigma_hat_j):
    """if the coefficient is positive, we need to compute twice the
    probability of seeing an even larger value; otherwise twice the
    probability of seeing a smaller value"""
    if beta_hat_j > 0:
        return 2 * (1 - probability.normal_cdf(beta_hat_j / sigma_hat_j))
    else:
        return 2 * probability.normal_cdf(beta_hat_j / sigma_hat_j)


def ridge_penalty(beta, alpha):
    """alpha is a hyper-parameter controlling how harsh the penalty
    is; sometimes called 'lambda' but that is already a Python keyword"""
    return alpha * algebra.dot(beta[1:], beta[1:])


def squared_error_ridge(x_i, y_i, beta, alpha):
    """estimate error plus ridge penalty on beta"""
    return error(x_i, y_i, beta) ** 2 + ridge_penalty(beta, alpha)


def ridge_penalty_gradient(beta, alpha):
    """gradient of just the ridge penalty"""
    return [0] + [2 * alpha * beta_j for beta_j in beta[1:]]


def sqared_error_ridge_gradient(x_i, y_i, beta, alpha):
    """the gradient corresponding to the ith squared error term
    including the ridge penalty"""
    return algebra.vector_add(squared_error_gradient(x_i, y_i, beta),
                              ridge_penalty_gradient(beta, alpha))


def estimate_beta_ridge(x, y, alpha):
    """use gradient descent to fit a ridge regression with penalty alpha"""
    beta_initial = [random.random() for x_i in x[0]]
    return gradient.minimize_stochastic(partial(squared_error_ridge,
                                                alpha=alpha),
                                        partial(squared_error_gradient,
                                                alpha=alpha),
                                        x,
                                        y,
                                        beta_initial,
                                        0.001)


def lasso_penalty(beta, alpha):
    return alpha * sum(abs(beta_i) for beta_i in beta[1:])
