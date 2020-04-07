"""
Name: Dunn and Tupper Perfect Fluid
Coordinates: Cartesian
"""
from sympy import diag, exp, symbols

coords = symbols("t x y z", real=True)
variables = symbols("b", constant=True)
functions = ()
t, x, y, z = coords
b = variables
metric = diag(
    -1,
    4 * t ** 2 / (-b * (1 + b)),
    t ** (-2 * b) * exp(-4 * x),
    t ** (-2 * b) * exp(4 * x),
)
