"""
Name: Levi-Civita
References: Stephani (Table 16.2) p188
Coordinates: Cylindrical
Notes: Class A3
"""
from sympy import diag, symbols

coords = symbols("t r phi z", real=True)
variables = ()
functions = ()
t, r, ph, z = coords
metric = diag(-1 / z, z ** 2, z ** 2 * r ** 2, z)
