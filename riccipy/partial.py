from collections import deque
from sympy import Basic, Expr, Mul, S, Symbol, diff
from sympy.core.decorators import call_highest_priority
from sympy.tensor.tensor import (
    Tensor as SympyTensor,
    TensorHead,
    TensorSymmetry,
    TensMul,
)

from .tensor import Tensor, Index, IndexedTensor


class DiffOperator(Expr):
    _op_priority = 12
    is_commutative = False

    def __new__(cls, *args, left=S.One):
        if left == S.Zero:
            return S.Zero
        obj = Basic.__new__(cls, *args)
        obj._left = left
        return obj

    def __repr__(self):
        syms = [s.name for s in self.args]
        name = "\u2202(%s)" % ",".join(syms)
        return str(Mul(self._left, Symbol(name, commutative=False)))

    def __str__(self):
        return self.__repr__()

    @call_highest_priority("__rmul__")
    def __mul__(self, other):
        if isinstance(other, DiffOperator):
            args = self.args + other.args
            return DiffOperator(*args)
        return Mul(self._left, diff(other, *self.args)).doit()

    @call_highest_priority("__mul__")
    def __rmul__(self, other):
        return DiffOperator(*self.args, left=Mul(other, self._left))


class PartialDerivative(Tensor):
    is_TensorDerivative = True

    def __new__(cls, metric, **kwargs):
        basis = list(map(DiffOperator, metric.coords))
        return super().__new__(
            cls, "\u2202", basis, metric, comm="partial", covar=(-1,)
        )

    def __call__(self, idx):
        if idx.is_up:
            raise ValueError("partial derivatives cannot have a contravariant index")
        return IndexedPartial(self, [idx])

    def __repr__(self):
        return self._print()

    def __str__(self):
        return self.__repr__()


class IndexedPartial(IndexedTensor):
    _op_priority = 13

    @call_highest_priority("__rmul__")
    def __mul__(self, other):
        if not isinstance(other, TensMul):
            return SympyTensor.__mul__(self, other)
        expr = S.Zero
        terms = deque(other.args)
        for _ in range(len(terms)):
            terms.rotate(-1)
            leib, *niz = terms
            expr += TensMul(*niz, self * leib)
        return expr.doit()


class CovariantHead(TensorHead):
    is_TensorDerivative = True

    def __new__(cls, metric, **kwargs):
        sym = TensorSymmetry.fully_symmetric(1)
        obj = TensorHead.__new__(cls, "\u2207", [metric], sym, comm="partial")
        return obj

    def __call__(self, idx):
        return CovariantDerivative(self, [idx])


class CovariantDerivative(SympyTensor):
    _op_priority = 13
    is_TensorDerivative = True

    def __new__(cls, head, idx, left=S.One, **kwargs):
        obj = super().__new__(cls, head, idx, **kwargs)
        obj._head = head
        obj._idx = idx[0]
        obj._left = left
        return obj

    @call_highest_priority("__rmul__")
    def __mul__(self, other):
        metric = self._head.index_types[0]
        dum0 = Index(self._idx.name + "_0", metric)
        dum1 = Index(self._idx.name + "_1", metric, is_up=False)
        partial = metric.partial
        Gamma = metric.christoffel
        free_idxs = other.get_free_indices()
        coidx = self._idx
        if self._idx.is_up:
            coidx = dum1
        expr = partial(coidx) * other
        for idx in free_idxs:
            if idx.is_up:
                expr += Gamma(idx, coidx, -dum0) * other.substitute_indices((idx, dum0))
            else:
                expr -= Gamma(dum0, coidx, idx) * other.substitute_indices((idx, -dum0))
        left = self._left
        if self._idx.is_up:
            left *= metric(-coidx, self._idx)
        return TensMul(left, expr).doit()

    @call_highest_priority("__mul__")
    def __rmul__(self, other):
        left = TensMul(other, self._left).doit()
        return CovariantDerivative(self._head, [self._idx], left=left)

    def __repr__(self):
        tensor = SympyTensor(self._head, [self._idx])
        # TODO: Add printing support.
        return str(TensMul(self._left, tensor).doit())

    def __str__(self):
        return self.__repr__()
