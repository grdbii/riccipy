"""
Levi-Civita solution, Class BII
Stephani (Table 16.2) p188
"""
from sympy import diag, sinh, symbols

coords = symbols('t z r phi', real=True)
variables = symbols('M', constant=True)
functions = ()
t, z, r, ph = coords
M = variables
metric = diag(-z ** 2 * sinh(r) ** 2, 1 / (2 * M / z - 1), z ** 2, 2 * M / z - 1)