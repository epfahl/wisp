"""Defines the default environment and function for initializing the
environment.
"""


import operator as op
import math
import toolz as tz


def apply_fn(fn):
    """Return a function that applies fn to *args.
    """
    return lambda *args: fn(args)


def apply_reduce(fn):
    """Return a function that reduces *args with the given fn.
    """
    return lambda *args: reduce(fn, args)


def apply_comp(boolop, boolred):
    """Given a boolean binary operation and a boolean reduction (any/all),
    return a new function that returns True if the boolean reduction of all
    adjacent pairs in a sequence satisfy the boolean operator.
    """
    if boolred.__name__ not in ('any', 'all'):
        raise ValueError(
            "boolean reduction {} not recognized".format(boolred.__name__))
    return lambda *args: boolred(
        boolop(x, y) for x, y in zip(args[:-1], args[1:]))


MATH = tz.merge({
    '*': apply_reduce(op.mul),
    '+': apply_fn(sum),
    '/': apply_reduce(op.div),
    '-': apply_reduce(op.sub),
    '=': apply_comp(op.eq, all),
    'abs': abs,
    'min': apply_fn(min),
    'max': apply_fn(max)},
    {n: f for n, f in vars(math).iteritems() if not n.startswith('_')})


INEQUALITY = {
    '!=': apply_comp(lambda x, y: not op.eq(x, y), any),
    '>': apply_comp(op.gt, all),
    '<': apply_comp(op.lt, all),
    '>=': apply_comp(op.ge, all),
    '<=': apply_comp(op.le, all)}


LOGICAL = {
    'and': apply_fn(all),
    'or': apply_fn(any),
    'not': op.not_}


LIST = {
    'in': lambda x, y: op.contains(y, x),
    'list': apply_fn(list),
    'first': lambda x: x[0],
    'rest': lambda x: x[1:],
    'last': lambda x: x[-1]}


def init(**kwargs):
    """Return the initialized environment, where the default environment is
    merged with the user-defined mapping.
    """
    return tz.merge(
        MATH,
        INEQUALITY,
        LOGICAL,
        LIST,
        kwargs)
