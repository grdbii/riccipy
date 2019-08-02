"""
RicciPy
=======

Python library for tensor manipulation in General Relativity
"""

__version__ = "0.1-alpha"
from .metric import Metric, SpacetimeMetric, load_metric
from .numerical import lambdify_tensor
from .tensor import Index, Tensor, expand_array, expand_tensor, indices
