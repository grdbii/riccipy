"""
Name: Einstein
References: Stephani (10.23a) p122
Coordinates: Spherical
Symmetry: Static
"""
from sympy import diag, sin, symbols

coords = symbols("t r theta phi", real=True)
variables = symbols("Lambda", constant=True)
functions = ()
t, r, th, ph = coords
La = variables
metric = diag(-1, 1 / (1 - La * r ** 2), r ** 2, r ** 2 * sin(th) ** 2)
