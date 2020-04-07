"""
Name: Minkowski
Coordinates: Cartesian
Symmetry: Maximal
"""
from sympy import diag, symbols

coords = symbols("t x y z", real=True)
variables = ()
functions = ()
metric = diag(-1, 1, 1, 1)
