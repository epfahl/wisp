import operator as op
import pyparsing as pp


def apply_fn(fn):
    """Return a function that applies fn to *args.
    """
    return lambda *args: fn(args)


def apply_reduce(fn):
    """Return a function that reduces *args with the given fn.
    """
    return lambda *args: reduce(fn, args)


def all_equal(*args):
    """Return True if all the args are equal.
    """
    return args.count(args[0]) == len(args)


def not_all_equal(*args):
    """Return True if not all the args are equal.
    """
    return not all_equal(*args)


def all_comp(op, proc=all):
    """Return a function that returns True if all adjacent pairs satisfy the
    boolean operator.

    Notes
    -----
    * Replace all_equal and not_all_equal with this?
    """
    return lambda *args: proc(op(x, y) for x, y in zip(args[:-1], args[1:]))


ENV_DEFAULT = op_map = {
    '*': apply_reduce(op.mul),
    '+': apply_reduce(op.add),
    '/': apply_reduce(op.div),
    '-': apply_reduce(op.sub),
    'abs': op.abs,
    '=': all_comp(op.eq),
    '!=': all_comp(lambda x, y: not op.eq(x, y), any),
    '>': all_comp(op.gt),
    '<': all_comp(op.lt),
    '>=': all_comp(op.ge),
    '<=': all_comp(op.le),
    'and': apply_fn(all),
    'or': apply_fn(any),
    'not': op.not_,
    'in': lambda x, y: op.contains(y, x),
    'list': apply_fn(list)}


def _parser(env):
    """Return an s-expression parser that resolves environment variables,
    numbers, and literals.
    """
    envval = pp.oneOf(env.keys()).setParseAction(lambda t: env[t[0]])
    number = pp.pyparsing_common.number
    boolean = pp.oneOf(("true", "false")).setParseAction(
        lambda t: True if t[0] == "true" else False)
    null = pp.Word("null").setParseAction(lambda t: None)
    char = pp.Word(pp.alphas + "_")
    return pp.nestedExpr(
        content=pp.OneOrMore(number | boolean | envval | null | char))


def parse(expr, env):
    """Return the list representation of a single nested s-expression.
    """
    return _parser(env).parseString(expr).asList()[0]


def evaluate(x):
    if isinstance(x, list):
        if callable(x[0]):
            return x[0](*map(evaluate, x[1:]))
        elif x[0] == 'if':
            return evaluate(x[2] if evaluate(x[1]) else x[3])
        else:
            raise ValueError("invalid prefix: '{}'".format(x[0]))
    else:
        return x


def run(expr, env=ENV_DEFAULT):
    return evaluate(parse(expr, env))
