# wisp
A tiny Lisp calculator written in Python.

## What can it do?

After importing wisp into your namespace, try:

```python
>>> wisp.eval("(+ 1 2 3)")
6
```

Too simple?  Here's something a little more involved:

```python
>>> expr = """
(if 
	(> (first (list 3 2 1)) 1)
	(* (- 3 1) 2)
	false)
"""
>>> wisp.eval(expr)
"4"
```

The default environment has basic arithmetic operations `(* + / - abs)`, numerical comparisons `(= != > < >= <=)`, logical operators `(and or not in)`, and primitive list operations `(list first rest last)`.  See the tests for examples of how these functions work in practice.

The only special form (i.e., a symbol that requires special handling) is `if`, which has the usual Lisp syntax: `(if <boolean expression> <consequence if true> <alternative>)`.


## What's the catch?

You might have already guessed...  There's no `define` or `lambda` or `let`.  This means that there's no way to modify the environment after an expression has been parsed and evaluated.  So, no bindings or functions defined at runtime.  

At the time an expression is parsed, each symbol is replaced with either a numeric literal, a boolean literal ('true' -> True, 'false' -> False), a value from the environment, a null literal ('null' -> None), or a string literal for symbols that couldn't be parsed otherwise.  A parsed expression is a nesting of Python lists, which is then evaluated recursively.

For an awesome tutorial on how to build a more complete Lisp/Schema interpreter in Python, see [Peter Norvig's page](http://norvig.com/lispy.html).  If you want to experience the full power of (Clojure-flavored) Lisp from the comfort of your Python environment, take [hylang](http://docs.hylang.org/) for a spin.     


## Why was this built?

Two reasons:

1) Lisp is data.  That is, Lisp code is just a string that directly represents the abstract syntax tree.  Suppose you have an API with a configuration that requires the specification of abstract boolean expressions.  With Lisp, serialization and sharing of such expressions is trivial.  This would be awkward in Python. 

2) Safety.  By disallowing a dynamic runtime environment, it is not possible to define and execute arbitrary code.  Consumer-specified functions must be defined in the environment before an expression is evaluated.

