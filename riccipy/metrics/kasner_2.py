"""
Name: Kasner Vacuum
Coordinates: Cartesian
Symmetry: Axial
"""
from sympy import diag, symbols

coords = symbols("t x y z", real=True)
variables = ()
functions = ()
t, x, y, z = coords
metric = diag(-1, t ** 2, 1, 1)
