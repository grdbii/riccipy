"""
Name: Flat Boost Isotropy
References: Stephani (11.16) p128
Symmetry: Boost Rotation
Notes: Temporal Hyperbolic Sine
"""
from sympy import Function, diag, sinh, symbols

coords = symbols("t w x y", real=True)
variables = ()
functions = symbols("alpha beta", cls=Function)
t, w, x, y = coords
al, be = functions
metric = diag(-be(w) ** 2 * sinh(y) ** 2, 1, al(w) ** 2, be(w) ** 2)
