RicciPy
=======

|pypi version| |Build status|

.. |pypi version| image:: https://img.shields.io/pypi/v/riccipy.svg
.. |Build status| image:: https://travis-ci.org/cjayross/riccipy.svg?branch=master
    :target: https://travis-ci.org/cjayross/riccipy

A tensor algebra calculator for General Relativity.

Usage
-----

RicciPy makes extensive usage of ``sympy`` for managing tensor products and
contractions. To create a tensor, it is required to construct a means of
representing the components of the tensor. This can be done by using most
nested array types: a nested python list, a ``sympy.Array`` or ``sympy.Matrix``
instance, or a numpy array will work.

Before beginning any involved application, however, it is first necessary to
define a ``Metric`` instance so that indices can be appropriately raised and
lowered automatically.

In the following example, the electromagnetic tensor is used in a simple
calculation in a Minkowski spacetime:

.. code-block:: python

  >>> from sympy import diag, symbols
  >>> from einsteinpy.symbolic.tensor import Tensor, indices, expand_array
  >>> from einsteinpy.symbolic.metric import Metric
  >>> E1, E2, E3, B1, B2, B3 = symbols('E1:4 B1:4')
  >>> em = [[0, -E1, -E2, -E3],
            [E1, 0, -B3, B2],
            [E2, B3, 0, -B1],
            [E3, -B2, B1, 0]]
  >>> t, x, y, z = symbols('t x y z')

In the following the Minkowski metric is defined along with the ``Tensor``
object for the electromagnetic tensor using ``em`` for the components. Here,
the ``symmetry`` keyword in the constructor for the ``Tensor`` object is
optional but is used here to declare the tensor as being antisymmetric
(refer to sympy's documentation for the ``sympy.tensor.tensor`` module).

.. code-block:: python

  >>> eta = Metric('eta', [t, x, y, z], diag(1, -1, -1, -1))
  >>> F = Tensor('F', em, eta, symmetry=[[2]])
  >>> mu, nu = indices('mu nu', eta)

``mu`` and ``nu`` are now variables that can be used to represent the
indices of either the metric, ``eta``, or the tensor ``F``. Negative signs
indicate that the particular index is a subscript (covariant) rather than
a superscript (contravariant).

This first calculation demonstrates how contractions are handled---simply
multiply two indexed tensors and matching indices will automatically apply
the Einstein summation convention. Symbolically, indices that are to be
contracted are denoted by the metric those indices belong to (in this case
``eta_0`` and ``eta_1``).

To convert a symbolic tensor expression into components, pass the expression
to ``expand_array``.

.. code-block:: python

  >>> expr = F(mu, nu) * F(-mu, -nu)
  >>> expr
  F(eta_0, eta_1)*F(-eta_0, -eta_1)
  >>> expand_array(expr)
  2*B_1**2 + 2*B_2**2 + 2*B_3**2 - 2*E_1**2 - 2*E_2**2 - 2*E_3**2

This next calculation tested here demonstrates the consequence of having
defined ``F`` as being antisymmetric.

.. code-block:: python

  >>> expr = F(mu, nu) + F(nu, mu)
  >>> expand_array(expr)
  0

Metrics Database
****************

RicciPy comes with over 100 different metrics representing solutions to the
Einstein Field Equations. They currently can be viewed in the
``riccipy/metrics`` directory of the source, however, development is underway
to make searching these metrics easier. For the time being, the ``load_metric``
function can be used to automatically return a ``Metric`` instance of the
specified metric.

For example, to load an Anti de-Sitter spacetime, the call would look like:

.. code-block:: python

   >>> g = load_metric('g', 'anti_de_sitter_1')
   >>> g.as_array()
   [[-1, 0, 0, 0],
   [0, cos(t)**2, 0, 0],
   [0, 0, cos(t)**2*sinh(chi)**2, 0],
   [0, 0, 0, sin(theta)**2*cos(t)**2*sinh(chi)**2]]

Installation
------------

To install RicciPy the following dependencies are required:

   * Sympy (version >= 1.4)

   * Numpy (version >= 1.15)

Installation is handled automatically by using

.. code-block:: shell

   $ pip install riccipy

Contributing & Questions
------------------------

RicciPy is in it's early stages of development and thus contributions are
very welcome, yet they will be handled on a person-to-person basis until
sufficient interest accumulates in the project. Feel free to email the primary
author at ``calvinjayross@gmail.com`` if you have any questions or interest in
developing RicciPy.