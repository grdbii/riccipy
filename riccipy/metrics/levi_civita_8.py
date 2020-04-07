"""
Name: Levi-Civita Vacuum
References: Stephani (20.8) p221
Coordinates: Cylindrical
"""
from sympy import diag, symbols

coords = symbols("t rho phi z", real=True)
variables = symbols("m", constant=True)
functions = ()
t, rh, ph, z = coords
m = variables
metric = diag(
    -(rh ** (2 * m)),
    rh ** (2 * (m ** 2 - m)),
    rh ** (2 * (1 - m)),
    rh ** (2 * (m ** 2 - m)),
)
