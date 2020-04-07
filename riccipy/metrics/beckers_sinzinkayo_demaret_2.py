"""
Name: Beckers, Sinzinkayo, and Demaret
References: Beckers et al., Phys. Rev. D, v30, p1846, (1984)
Coordinates: Cartesian
Notes:
    - k = 1
    - d = 0
"""
from sympy import diag, symbols

coords = symbols("t x y z", real=True)
variables = symbols("m", constant=True)
functions = ()
t, x, y, z = coords
m = variables
expr = x ** (2 * m)
metric = diag(-expr, expr, expr, expr)
