from collections import defaultdict

from sympy import Array, preorder_traversal, simplify, symbols
from sympy.core.decorators import call_highest_priority
from sympy.tensor.array import permutedims, tensorcontraction, tensorproduct
from sympy.tensor.tensor import (
    TensMul,
    Tensor as SympyTensor,
    TensorHead,
    TensorIndex,
    TensorManager,
    TensorSymmetry,
)


class Repl(dict):
    """
    Dictionary object used for managing the replacements of tensors to arrays.
    """

    def getkey(self, tensor):
        item = tensor if (tensor.is_TensorHead or tensor.is_Metric) else tensor.args[0]
        for key in self.keys():
            if (key == item) or (key.args[0] == item):
                return key
        return None

    def haskey(self, tensor):
        key = self.getkey(tensor)
        return True if key is not None else False

    def setitem(self, tensor, array):
        key = self.getkey(tensor)
        if key is not None:
            return super().__setitem__(key, array)
        raise KeyError(str(tensor))

    def __setitem__(self, tensor, array):
        if self.haskey(tensor):
            return self.setitem(tensor, array)
        return super().__setitem__(tensor, array)


class AbstractTensor(object):
    """
    Wrapper class for sympy Array with attributes used for identification.
    """

    is_Tensor = True
    is_TensorHead = False
    is_Metric = False
    is_Spacetime = False
    is_TensorDerivative = False
    _array = None
    _inverse = None

    def __new__(cls, obj, matrix):
        obj._array = matrix
        obj._repl = Repl()
        return obj

    def as_matrix(self):
        """
        Return the data stored in the tensor as an instance of sympy.Matrix.

        Notes
        -----
        The ``tomatrix`` attribute required by this method will throw an error
        if the tensor is not of rank 2.
        """
        return self._array.tomatrix()

    def as_array(self):
        """
        Return the data stored in the tensor as an instance of sympy.Array.
        """
        return self._array.copy()

    def as_inverse(self):
        """
        Return the data of the inversed array associated with the tensor.
        """
        if self._inverse is None:
            self._inverse = Array(self.as_matrix().inv())
        return self._inverse


class IndexedTensor(AbstractTensor, SympyTensor):
    """
    Class representing a Tensor that has been evaluated with indices.

    Used as the base object for creating algebraic expressions with tensors.
    Inherited are methods such as __mul__ to allow sympy to manage dummy
    indices when multiplied with other tensors.

    Generated when a Tensor is called as a function with indices as arguments.
    """

    _op_priority = 11

    def __new__(cls, tensor, indices, **kwargs):
        obj = SympyTensor.__new__(cls, tensor, indices, **kwargs)
        array = tensor.covariance_transform(*indices)
        return AbstractTensor.__new__(cls, obj, array)

    @call_highest_priority("__rmul__")
    def __mul__(self, other):
        return SympyTensor.__mul__(self, other)

    @call_highest_priority("__mul__")
    def __rmul__(self, other):
        return SympyTensor.__rmul__(self, other)


class Tensor(AbstractTensor, TensorHead):
    """
    Class for representing a Sympy TensorHead object that have an associated
    array of data elements/expressions to be substituted when requested.
    """

    is_TensorHead = True

    def __new__(cls, symbol, matrix, metric, **kwargs):
        """
        Create a new Tensor object.

        Parameters
        ----------
        symbol : str
            Name of the tensor and the symbol to denote it by when printed.
        matrix : (list, tuple, sympy.Matrix, sympy.Array)
            Matrix representation of the tensor to be used in substitution.
            Can be of any type that is acceptable by sympy.Array.
        metric : Metric
            Classify the tensor as being defined in terms of a metric.

        Notes
        -----
        If the parameter ``symmetry`` is passed, the tensor object will defined
        using a specific symmetry specified as follows:
        ``(1)``         vector
        ``(2)``         tensor with 2 symmetric indices
        ``(-2)``        tensor with 2 antisymmetric indices
        ``(2, -2)``     tensor with the first 2 indices commuting and the last 2 anticommuting
        ``(1, 1, 1)``   tensor with 3 indices without any symmetry

        Additionally, the parameter ``covar`` indicates that the passed array
        corresponds to the covariance of the tensor it is intended to describe.

        Lastly, the parameter ``comm`` is used to indicate what commutation
        group the tensor belongs to. In other words, it describes what other
        types of tensors the one being created is allowed to commute with.
        There are three commutation groups: ``general`` for ordinary tensors,
        ``metric`` for metric tensors, and ``partial`` for partial derivatives.

        Examples
        --------
        >>> from sympy import diag, symbols
        >>> from riccipy import Metric, Tensor, indices, expand_array
        >>> E1, E2, E3, B1, B2, B3 = symbols('E1:4 B1:4')
        >>> em = [[0, -E1, -E2, -E3], [E1, 0, -B3, B2], [E2, B3, 0, -B1], [E3, -B2, B1, 0]]
        >>> t, x, y, z = symbols('t x y z')
        >>> eta = Metric('eta', [t, x, y, z], diag(1, -1, -1, -1))
        >>> F = Tensor('F', em, eta, symmetry=(-2,))
        >>> mu, nu = indices('mu nu', eta)
        >>> expr = F(mu, nu) + F(nu, mu)
        >>> expand_array(expr)
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        >>> expr = F(mu, nu) * F(-mu, -nu)
        >>> expand_array(expr)
        2*B1**2 + 2*B2**2 + 2*B3**2 - 2*E1**2 - 2*E2**2 - 2*E3**2
        """
        array = Array(matrix)
        sym = kwargs.pop("symmetry", array.rank() * (1,))
        sym = TensorSymmetry.direct_product(*sym)
        comm = kwargs.pop("comm", "general")
        covar = tuple(kwargs.pop("covar", array.rank() * (1,)))
        if len(covar) != array.rank():
            raise ValueError(
                "covariance signature {} does not match tensor rank {}".format(
                    covar, array.rank()
                )
            )

        obj = TensorHead.__new__(
            cls, symbol, array.rank() * [metric], sym, comm=comm, **kwargs
        )
        obj = AbstractTensor.__new__(cls, obj, array)
        # resolves a bug with pretty printing.
        obj.__class__.__name__ = "TensorHead"
        obj.covar = covar
        idxs = obj._dummy_idxs()
        obj._repl[obj(*idxs)] = array
        return obj

    def __repr__(self):
        return self._print()

    def __str__(self):
        return self.__repr__()

    def __call__(self, *args, **kwargs):
        new = IndexedTensor(self, args, **kwargs)
        return new.doit()

    def __getitem__(self, keys):
        return self._array.__getitem__(keys)

    def _dummy_idxs(self):
        count = defaultdict(int)

        def dummy_name_gen(idxtype):
            # generate a generic index for the entry in replacement dictionary.
            fmt = idxtype.dummy_name + "_%d"
            n = count[idxtype]
            count[idxtype] += 1
            return fmt % n

        idx_names = map(dummy_name_gen, self.index_types)
        idx_generator = map(Index, idx_names, self.index_types)
        idxs = [
            idx if self.covar[pos] > 0 else -idx
            for pos, idx in enumerate(idx_generator)
        ]
        return idxs

    def subs(self, sub_dict):
        """
        Use a dictionary to replace symbols/variables in a tensor.

        Parameters
        ----------
        sub_dict : dict
            Dictionary that maps symbols to expressions.

        Examples
        --------
        >>> from sympy import Rational, diag, exp, sin, symbols
        >>> from riccipy import Metric, indices
        >>> t, r, th, ph, M = symbols('t r theta phi M', real=True)
        >>> schwarzschild = diag(1 - 2 * M/r, 1/(1 - 2 * M/r), r ** 2, r ** 2 * sin(th) ** 2)
        >>> g = Metric('g', [t, r, th, ph], schwarzschild)
        >>> g.subs({M: Rational(1, 2)})
        >>> g.as_array()
        [[1 - 1/r, 0, 0, 0], [0, 1/(1 - 1/r), 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2*sin(theta)**2]]
        """
        self._array = self._array.subs(sub_dict)
        idxs = self._dummy_idxs()
        self._repl[self(*idxs)] = self._array

    def covariance_transform(self, *indices):
        """
        Return the array associated with this tensor with indices set according
        to arguments.

        Parameters
        ----------
        indices : TensorIndex
            Defines the covariance and contravariance of the returned array.

        Examples
        --------
        >>> from sympy import Function, diag, exp, sin, symbols
        >>> from riccipy import Metric, indices
        >>> t, r, th, ph = symbols('t r theta phi')
        >>> al, be = symbols('alpha beta', cls=Function)
        >>> spherical = diag(-exp(2 * al(r)), exp(2 * be(r)), r ** 2, r ** 2 * sin(th) ** 2)
        >>> g = Metric('g', [t, r, th, ph], spherical)
        >>> mu, nu = indices('mu nu', g)
        >>> g.covariance_transform(mu, nu)
        [[-exp(-2*alpha(r)), 0, 0, 0], [0, exp(-2*beta(r)), 0, 0], [0, 0, r**(-2), 0], [0, 0, 0, 1/(r**2*sin(theta)**2)]]
        """  # noqa: E501
        array = self.as_array()
        for pos, idx in enumerate(indices):
            if idx.is_up ^ (self.covar[pos] > 0):
                if idx.is_up:
                    metric = idx.tensor_index_type.metric.as_inverse()
                else:
                    metric = idx.tensor_index_type.metric.as_array()
                new = tensorcontraction(tensorproduct(metric, array), (1, 2 + pos))
                permu = list(range(len(indices)))
                permu[0], permu[pos] = permu[pos], permu[0]
                array = permutedims(new, permu)
        return array

    def simplify(self):
        """
        Replace the stored array associated with this tensor with a simplified
        version. This method also replaces the entry in the replacement dictionary.
        """
        array = self.as_array().applyfunc(simplify)
        self._array = array
        self._repl.setitem(self, array)
        return array


class Index(TensorIndex):
    """
    Class for a symbolic representation of a tensor index with respect to a metric.
    """

    def __new__(cls, symbol, metric, is_up=True, **kwargs):
        return super().__new__(cls, symbol, metric, is_up=is_up, **kwargs)

    def __neg__(self):
        return Index(self.name, self.tensor_index_type, (not self.is_up))


def expand_array(expr, idxs=None):
    """
    Evaluate a tensor expression and return the result as an array.

    Parameters
    ----------
    expr : TensExpr
        Symbolic expression of tensors.
    idxs : TensorIndex
        Indices that encode the covariance and contravariance of the result.
    """
    repl = Repl()

    for arg in preorder_traversal(expr):
        if isinstance(arg, AbstractTensor):
            repl.update(arg._repl)
            for metric in arg.index_types:
                repl.update(metric._repl)

    if idxs is None:
        idxs = TensMul(expr).get_free_indices()
    return expr.replace_with_arrays(repl, idxs)


def expand_tensor(symbol, expr, metric, idxs=None, **kwargs):
    """
    Evaluate a tensor expression and return the result as a tensor.

    Parameters
    ----------
    symbol : str
        Name of the tensor and the symbol to denote it by when printed.
    expr : TensExpr
        Symbolic expression of tensors.
    metric : Metric
        Classify the tensor as being defined in terms of a metric.
    idxs : TensorIndex
        Indices that encode the covariance and contravariance of the result.
    """
    result = expand_array(expr, idxs)
    if not isinstance(result, Array):
        return result
    if idxs is None:
        idxs = TensMul(expr).get_free_indices()
    covar = [1 if idx.is_up else -1 for idx in idxs]
    return Tensor(symbol, result, metric, covar=covar, **kwargs)


def indices(s, metric, is_up=True):
    """
    Create indices using a method similar to sympy.symbols.
    """
    if isinstance(s, str):
        a = [x.name for x in symbols(s, seq=True)]
    else:
        raise ValueError(
            "expected a string, received object of type {}".format(type(s))
        )
    idxs = [Index(idx, metric, is_up) for idx in a]
    if len(idxs) == 1:
        return idxs[0]
    return idxs


# metric tensors and general tensors commute with each other and themselves.
TensorManager.set_comm("general", "general", 0)
# partial derivatives only commute with themselves.
TensorManager.set_comm("partial", "partial", 0)
