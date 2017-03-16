import operator as op
import pyparsing as pp


def apply_fn(fn):
    return lambda *args: fn(args)


def apply_reduce(fn):
    return lambda *args: reduce(fn, args)


def all_equal(*args):
    return args.count(args[0]) == len(args)


def not_all_equal(*args):
    return not all_equal(*args)


ENV_DEFAULT = op_map = {
    '=': all_equal,
    '!=': not_all_equal,
    '*': apply_reduce(op.mul),
    '+': apply_reduce(op.add),
    '/': apply_reduce(op.div),
    '-': apply_reduce(op.sub),
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le,
    'abs': op.abs,
    'and': apply_fn(all),
    'or': apply_fn(any),
    'not': op.not_,
    'contains': op.contains}


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
