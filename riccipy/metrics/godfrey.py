"""
Name: Godfrey
References:
    - Godfrey, Gen. Rel. Grav., v3, p3, (1972)
    - McIntosh, Gen. Rel. Grav., v7, p199-213, (1976)
Coordinates: Cylindrical
Notes:
    - Nontrivial Homothety
    - Not Hypersurface Orthogonal
    - Null Homothetic Bivector
"""
from sympy import diag, exp, symbols

coords = symbols("t r phi z", real=True)
variables = symbols("a C")
functions = ()
t, r, ph, z = coords
a, C = variables
expr = r ** (2 * a * (a - 1)) * exp(2 * (2 * a * z - z - r ** 2 / 2 + C))
metric = diag(-(r ** (2 * a)) * exp(2 * z), expr, r ** (2 * (1 - a)) / exp(2 * z), expr)
