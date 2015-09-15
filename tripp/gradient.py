import logging

logging.basicConfig(level=logging.INFO, format="%(lineno)d\t%(message)s")


def sum_of_squares(v):
    """computes the sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)


def difference_quotient(f, x, h):
    """the limit of the difference quotients"""
    return (f(x + h) - f(x)) / h


def step(v, direction, step_size):
    """move step_size in the direction from v"""
    return [v_i + step_size * direction_i
            for v_i, direction_i in zip(v, direction)]


def sum_of_squares_gradient(v):
    return [2 * i for i in v]


def safe(f):
    """return a new function that's the same as f,
    except that it outputs infinity whenever f
    returns an error"""
    def safe_f(*args, **kwargs):
        """docstring for safe_f"""
        try:
            return f(*args, **kwargs)
        except:
            return float('inf')
    return safe_f


def minimize_batch(target_fn, gradient_fn, theta_0, tolerance=0.0000001):
    """use gradient descent to find theta
    that minimizes target function"""
    step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]

    theta = theta_0
    target_fn = safe(target_fn)
    value = target_fn(theta)

    while True:
        _gradient = gradient_fn(theta)
        next_thetas = [step(theta, _gradient, -step_size)
                       for step_size in step_sizes]

        # choose the one that minimizes the error function
        next_theta = min(next_thetas, key=target_fn)
        next_value = target_fn(next_theta)

        if abs(value - next_value) < tolerance:
            return theta
        else:
            theta, value = next_theta, next_value
