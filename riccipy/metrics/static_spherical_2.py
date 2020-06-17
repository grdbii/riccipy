"""
Name: Generic Static Spherical
References: Stephani (14.1) p163
Coordinates: Spherical
Symmetry:
    - Spherical
    - Static
Notes: Additional exponential factors
"""
from sympy import Function, diag, exp, sin, symbols

coords = symbols("t r theta phi", real=True)
variables = ()
functions = symbols("alpha beta", cls=Function)
t, r, th, ph = coords
alpha, beta = functions
metric = diag(
    -exp(2 * alpha(r)),
    exp(2 * beta(r)),
    exp(2 * beta(r)) * r ** 2,
    exp(2 * beta(r)) * r ** 2 * sin(th) ** 2,
)
