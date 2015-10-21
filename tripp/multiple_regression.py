from algebra import dot
import gradient
import probability
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
