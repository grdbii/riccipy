"""
Name: Minkowski
Coordinates: 'Null'
Symmetry: Maximal
"""
from sympy import Rational, sin, symbols, zeros

coords = symbols("u v theta phi", real=True)
variables = symbols("a b c", constant=True)
functions = ()
u, v, th, ph = coords
a, b, c = variables
metric = zeros(4)
metric[2, 2] = (a * u - Rational(1, 2) * v / a + c) ** 2
metric[3, 3] = (a * u - Rational(1, 2) * v / a + c) ** 2 * sin(th) ** 2
metric[0, 1] = metric[1, 0] = -1
