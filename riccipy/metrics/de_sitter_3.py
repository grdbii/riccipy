"""
Name: de Sitter
References: Hawking and Ellis p125
Coordinates: Spherical
Symmetry: Maximal
Notes: Cosmological Constant
"""
from sympy import diag, sin, symbols

coords = symbols("t r theta phi", real=True)
variables = symbols("Lambda", constant=True)
functions = ()
t, r, th, ph = coords
La = variables
expr = 1 - La * r ** 2 / 3
metric = diag(-expr, 1 / expr, r ** 2, r ** 2 * sin(th) ** 2)
