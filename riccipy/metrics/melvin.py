"""
Name: Melvin Magnetic Universe
References:
    - Bonnor, Prog. Roy. Soc. Lond., vA67, p225, (1954)
    - Melvin, Phys. Lett., v8, p65, (1964)
    - Stephani (20.10) p222
Coordinates: Cylindrical
"""
from sympy import diag, symbols

coords = symbols("t rho phi z", real=True)
variables = symbols("B_0", constant=True)
functions = ()
t, rh, ph, z = coords
B0 = variables
expr = (1 + B0 ** 2 * rh ** 2 / 4) ** 2
metric = diag(-expr, expr, rh ** 2 / expr, expr)
