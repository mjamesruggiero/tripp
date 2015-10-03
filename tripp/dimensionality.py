import algebra
import gradient
from functools import partial


def direction(w):
    mag = algebra.magnitude(w)
    return [w_i / mag for w_i in w]


def directional_variance_i(x_i, w):
    """the variance of the row x_i in the direction determined by w"""
    return algebra.dot(x_i, direction(w)) ** 2


def directional_variance(X, w):
    """the variance of the data in the direction determined w"""
    return sum(directional_variance_i(x_i, w) for x_i in X)


def directional_variance_gradient_i(x_i, w):
    """the contribution of row x_i
    to the gradient of the direction-w variance"""
    projection_length = algebra.dot(x_i, direction(w))
    return [2 * projection_length * x_ij for x_ij in x_i]


def directional_variance_gradient(X, w):
    return algebra.vector_sum(directional_variance_gradient_i(x_i, w)
                              for x_i in X)


def first_principal_component(X):
    """the direction that maximizes the directional_variance function"""
    guess = [1 for _ in X[0]]
    unscaled_maximizer = gradient.maximize_batch(
        partial(directional_variance, X),
        partial(directional_variance_gradient, X),
        guess
    )
    return direction(unscaled_maximizer)


def first_principal_component_sgd(X):
    """there is no 'y' value, so we pass in a vector of Nones
    and functions that ignore that input"""
    guess = [1 for _ in X[0]]
    unscaled_maximizer = gradient.maximize_stochastic(
        lambda x, _, w: directional_variance_i(x, w),
        lambda x, _, w: directional_variance_gradient_i(x, w),
        X,
        [None for _ in X],
        guess)
    return direction(unscaled_maximizer)
