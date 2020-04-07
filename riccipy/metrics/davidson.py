"""
Name: Davidson Perfect Fluid
References: Davidson, J. Math. Phys., v32, p1560, (1991)
Coordinates: Cylindrical
Symmetry: Cylindrical
"""
from sympy import Rational, diag, symbols

coords = symbols("t r phi z", real=True)
variables = ()
functions = ()
t, r, phi, z = coords
expr = (1 + r ** 2) ** Rational(2, 5)
metric = diag(
    -(expr ** 3),
    t ** Rational(4, 3) * expr,
    t ** Rational(4, 3) * r ** 2 / expr,
    t ** Rational(-2, 3) / expr,
)
