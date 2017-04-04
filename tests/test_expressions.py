import wisp

# List of (expression, return value).
EXPRESSIONS = [

    ("(+ 1 2 3)", 6),
    ("(- 1 2 3)", -4),
    ("(* 1 2 3)", 6),
    ("(/ 3.0 2.0)", 1.5),
    ("(abs -1)", 1),

    ("(> 3 2 1)", True),
    ("(< 3 2 1)", False),
    ("(>= 3 2 2)", True),
    ("(<= 2 2 3)", True),
    ("(= 1 1 1)", True),
    ("(= 1 2 1)", False),
    ("(!= 1 1 1)", False),
    ("(!= 1 1 2)", True),

    ("(and true true)", True),
    ("(and true false)", False),
    ("(and false false)", False),
    ("(or true false)", True),
    ("(or true true)", True),
    ("(or false false)", False),
    ("(not true)", False),
    ("(not false)", True),

    ("(list 1 2 3)", [1, 2, 3]),
    ("(first (list 1 2 3))", 1),
    ("(rest (list 1 2 3))", [2, 3]),
    ("(last (list 1 2 3))", 3),

    ("(* (+ 1 2) (- 3 1))", 6),
    ("(in 1 (list 1 2 3))", True),
    ("(and (>= 3 2 2) (< 1 2))", True),
    ("(if (> 2 1) (abs -1) (+ 1 1))", 1),
    ("(if (> 1 2) 0 (+ 1 1))", 2),

]


def test_expressions():
    for e, r in EXPRESSIONS:
        assert wisp.eval(e) == r
