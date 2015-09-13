def sum_of_squares(v):
    """computes the sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)

def difference_quotient(f, x, h):
    """the limit of the difference quotients"""
    return (f(x + h) - f(x)) / h
