"""
Name: Levi-Civita
References: Stephani (Table 16.2) p188
Coordinates: Cylindrical
Notes: Class B3
"""
from sympy import diag, symbols

coords = symbols("t r phi z", real=True)
variables = ()
functions = ()
t, r, ph, z = coords
metric = diag(-(r ** 2) * z ** 2, z ** 2, 1 / z, z)
