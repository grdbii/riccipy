"""
Name: Bianchi IV
Coordinates: Cartesian
"""
from sympy import Function, diag, exp, symbols

coords = symbols("t x y z", real=True)
variables = ()
functions = symbols("alpha beta gamma", cls=Function)
t, x, y, z = coords
alpha, beta, gamma = functions
metric = diag(1, exp(alpha(t)), exp(beta(t)), exp(gamma(t)))
