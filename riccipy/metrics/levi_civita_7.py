"""
Name: Levi-Civita Vacuum
References: Stephani (20.8) p221
Coordinates: Cylindrical
Notes: m = 2
"""
from sympy import diag, symbols

coords = symbols("t rho phi z", real=True)
variables = ()
functions = ()
t, rh, ph, z = coords
metric = diag(-(rh ** 4), rh ** 4, 1 / rh ** 2, rh ** 4)
