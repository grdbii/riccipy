"""
Name: Levi-Civita
References: Stephani (Table 16.2) p188
Coordinates: Cylindrical
Notes: Class B2
"""
from sympy import diag, sinh, symbols

coords = symbols("t r phi z", real=True)
variables = symbols("M", constant=True)
functions = ()
t, r, ph, z = coords
M = variables
metric = diag(-(z ** 2) * sinh(r) ** 2, z ** 2, 2 * M / z - 1, 1 / (2 * M / z - 1))
