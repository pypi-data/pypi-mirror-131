import numpy as np


def to_db(value):
    """Convert from linear to logarithmic."""
    return 10 * np.log10(value)


def from_db(logvalue):
    """Convert from logarithmic to linear."""
    return 10 ** (logvalue/10)


def make_callable(param):
    """
    Creates a callable.

    If `param` is already callable (a function) then it will just be
    returned. If `param` is a constanct, it will be wrapped into a
    lambda function.
    """
    return param if callable(param) else lambda *args, **kwargs: param
