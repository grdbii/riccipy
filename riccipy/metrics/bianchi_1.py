"""
Name: Bianchi II
Coordinates: Cartesian
"""
from sympy import Function, diag, exp, symbols

coords = symbols("t x y z", real=True)
variables = ()
functions = symbols("alpha", cls=Function)
t, x, y, z = coords
alpha = functions
metric = diag(1, exp(-2 * alpha(t)), exp(alpha(t)), exp(alpha(t)))
