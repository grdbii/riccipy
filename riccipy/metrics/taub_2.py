"""
Name: Taub Vacuum
References: Taub, Ann. Math., v53, p473, (1951)
Coordinates: Cartesian
Symmetry: Planar
"""
from sympy import diag, sqrt, symbols

coords = symbols("t x y z", real=True)
variables = ()
functions = ()
t, x, y, z = coords
metric = diag(-1 / sqrt(z), z, z, 1 / sqrt(z))
