"""
RicciPy
=======

Python library for tensor manipulation in General Relativity
"""

from .metric import Metric, SpacetimeMetric, load_metric
from .numerical import lambdify_tensor
from .tensor import Index, Tensor, expand_array, expand_tensor, indices

__all__ = [
    "Metric",
    "SpacetimeMetric",
    "load_metric",
    "lambdify_tensor",
    "Index",
    "Tensor",
    "expand_array",
    "expand_tensor",
    "indices",
]
