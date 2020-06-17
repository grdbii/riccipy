"""
Name: Bianchi
References: Stephani (13.49) p162
Coordinates: Cartesian
Symmetry: Planar
Notes: Bianchi I
"""
from sympy import Function, diag, exp, symbols

coords = symbols("t x y z", real=True)
variables = ()
functions = symbols("alpha beta", cls=Function)
t, x, y, z = coords
alpha, beta = functions
metric = diag(-1, exp(2 * beta(t)), exp(2 * beta(t)), exp(2 * alpha(t)))
