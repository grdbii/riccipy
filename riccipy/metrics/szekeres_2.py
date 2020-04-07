"""
Name: Szekeres Stiff Perfect Fluid
References: Szekeres, Commun. Math. Phys., v41, p55, (1975)
Coordinates: Cartesian
Notes: Abelian Coordinates
"""
from sympy import cosh, diag, exp, symbols

coords = symbols("t x y z", real=True)
variables = ()
functions = ()
t, x, y, z = coords
metric = diag(
    -exp(6 * x) / cosh(2 * t) ** 2,
    exp(6 * x) / cosh(2 * t) ** 2,
    exp(2 * x) * cosh(2 * t),
    exp(2 * x) * cosh(2 * t),
)
