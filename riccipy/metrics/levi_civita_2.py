"""
Name: Levi-Civita
References: Stephani (Table 16.2) p188
Coordinates: Cylindrical
Notes: Class A2
"""
from sympy import diag, sinh, symbols

coords = symbols("t r phi z", real=True)
variables = symbols("M", constant=True)
functions = ()
t, r, ph, z = coords
M = variables
metric = diag(-(2 * M / z - 1), z ** 2, z ** 2 * sinh(r) ** 2, 1 / (2 * M / z - 1))
