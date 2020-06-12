Installation
============

You can install RicciPy using pip_:

.. code-block:: shell

    $ pip install [--user] riccipy

The installation depends heavily on SymPy_ and moderately on NumPy_.
Specifically, RicciPy requires Sympy 1.6 or later in order to work
properly, however this is handled automatically by ``pip``.

RicciPy is tested to work with Python versions 3.6 and later.

Developer Installation
----------------------

If you are intending to contribute or modify to RicciPy, it is recommended
that you use a slight modification to the above ``pip`` command:

.. code-block:: shell

    $ pip install [--user] -e <path to RicciPy repo>


.. _SymPy: https://www.sympy.org/en/index.html
.. _NumPy: https://numpy.org/
.. _pip: https://pip.pypa.io/en/stable/
