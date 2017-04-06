"""Defines the parser orbect and the parse function.
"""

import pyparsing as pp


def parser(env):
    """Given an environment, return an s-expression parser that resolves
    literals and environment variables.  The defined literals are

    * integer and float numbers
    * true and false to represent Python's True and False
    * null to represent Python's None
    * strings that are not environment keys
    """
    envval = pp.oneOf(env.keys()).setParseAction(lambda t: env[t[0]])
    number = pp.pyparsing_common.number
    true = pp.Keyword("true").setParseAction(pp.replaceWith(True))
    false = pp.Keyword("false").setParseAction(pp.replaceWith(False))
    null = pp.Keyword("null").setParseAction(pp.replaceWith(None))
    char = pp.Word(pp.alphas + "_")
    return pp.nestedExpr(content=pp.OneOrMore(
        number |
        true |
        false |
        null |
        envval |
        char))


def parse(expr, env):
    """Given an s-expression and an environment, return the nested list
    Python representation with all s-expression symbols resolved as literals
    or environment values.
    """
    return parser(env).parseString(expr).asList()[0]
