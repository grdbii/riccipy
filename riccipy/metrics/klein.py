"""
Name: Klein Radiation Perfect Fluid
Coordinates: Spherical
Symmetry:
    - Spherical
    - Static
"""
from sympy import Rational, diag, sin, sqrt, symbols

coords = symbols("t r theta phi", real=True)
variables = symbols("p_0", constant=True)
functions = ()
t, r, th, ph = coords
p0 = variables
metric = diag(-sqrt(7 * p0) * r, Rational(7, 4), r ** 2, r ** 2 * sin(th) ** 2)
