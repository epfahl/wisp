"""Main access module for wisp.
"""

from . import environment
from . import parsing


def evaluate(x):
    """Evaluate the nested list of resolved symbols.
    """
    if isinstance(x, list):
        if callable(x[0]):
            return x[0](*map(evaluate, x[1:]))
        elif x[0] == 'if':
            return evaluate(x[2] if evaluate(x[1]) else x[3])
        else:
            raise ValueError("invalid prefix: '{}'".format(x[0]))
    else:
        return x


def eval(expr, env=environment.init()):
    """Evaluate the given s-expression against the given environment.

    Examples
    --------
    >>> eval('(+ 1 1)')
    2
    >>> eval('(if (> 2 1) (abs -1) (+ 1 1))')
    1
    """
    return evaluate(parsing.parse(expr, env))
