from __future__ import division
from probability import normal_cdf, inverse_normal_cdf
import random
import math
import logging


logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def normal_approximation_to_binomial(n, p):
    """finds mu and sigma corresponding to a Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma

normal_probability_below = normal_cdf

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# probabilities that a normal lies in an interval
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def normal_probability_above(lo, mu=0, sigma=1):
    """above if it's not below the threshold"""
    return 1 - normal_cdf(lo, mu, sigma)


def normal_probability_between(lo, hi, mu=0, sigma=1):
    """between if less than hi but not less than lo"""
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


def normal_probability_outside(lo, hi, mu=0, sigma=1):
    """outside if it's not between"""
    return 1 - normal_probability_between(lo, hi, mu, sigma)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# normal bounds
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def normal_upper_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z <= z) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability, mu=0, sigma=1):
    """ireturns the z for which P(Z >= z) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)


def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """returns the symmetric (about the mean) bounds
    that contain the specified probability"""
    tail_probability = (1 - probability) / 2

    # upper bound should have tail probability above
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)

    lower_bound = normal_upper_bound(tail_probability, mu, sigma)

    return lower_bound, upper_bound


def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # if x is greater than the mean, tail is above x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, tail is below x
        return 2 * normal_probability_below(x, mu, sigma)


def count_extreme_values():
    extreme_value_count = 0
    for _ in range(100000):
        num_heads = sum(1 if random.random() < 0.5 else 0
                        for _ in range(1000))
        if num_heads >= 530 or num_heads <= 470:
            extreme_value_count += 1
    return extreme_value_count / 100000


upper_p_value = normal_probability_above
lower_p_value = normal_probability_below

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# P-hacking
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def run_experiment():
    """flip a fair coin 1000 times
    True = heads, False = tails"""
    return [random.random() < 0.5 for _ in range(1000)]


def reject_fairness(experiment):
    """using 5% significance tests"""
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 469 or num_heads > 531

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# running A/B test
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def estimated_parameters(N, n):
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma


def a_b_test_statistic(N_A, n_A, N_B, n_B):
    p_A, sigma_A = estimated_parameters(N_A, n_A)
    p_B, sigma_B = estimated_parameters(N_B, n_B)
    return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Bayesian inference
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def B(alpha, beta):
    """a normalizing constant so that the total probability is 1"""
    return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)


def beta_pdf(x, alpha, beta):
    if x < 0 or x > 1:
        return 0
    return x ** (alpha - 1) * (1 - x) ** (beta - 1) / B(alpha, beta)


if __name__ == '__main__':
    mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
    logging.info("mu_0\t{}".format(mu_0))
    logging.info("sigma_0\t{}".format(sigma_0))
    logging.info("normal_two_sided_bounds(0.95, mu_0, sigma_0)\t{}"
                 .format(normal_two_sided_bounds(0.95, mu_0, sigma_0)))

    logging.info("-----------------------------------------------")
    logging.info("95% bounds based on assumption that p is 0.5")
    lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
    logging.info("lo\t{}".format(lo))
    logging.info("hi\t{}".format(hi))

    logging.info("-----------------------------------------------")
    logging.info("actual mu and sigma based on p = 0.55")
    mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
    logging.info("mu_1\t{}".format(mu_1))
    logging.info("sigma_1\t{}".format(sigma_1))

    type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
    power = 1 - type_2_probability
    logging.info("type 2 probability\t{}".format(type_2_probability))
    logging.info("power\t{}".format(power))
