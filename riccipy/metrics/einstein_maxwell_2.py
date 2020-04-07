"""
Name: Einstein-Maxwell Field
References: Stephani (20.9a) p221
Coordinates: Cylindrical
Symmetry:
    - Cylindrical
    - Static
Notes: Longitudinal Magnetic Field
"""
from sympy import cosh, diag, log, symbols

coords = symbols("t rho phi z", real=True)
variables = symbols("a b m", constant=True)
functions = ()
t, rh, ph, z = coords
a, b, m = variables
expr1 = cosh(log(a * rh ** m)) ** 2
expr2 = rh ** (2 * m ** 2) * b ** 2 * expr1
metric = diag(-expr2, expr2, 1 / (b ** 2 * expr1), rh ** 2 * b ** 2 * expr1)
