from typing import Protocol, TypeVar


Lhs = TypeVar("Lhs", contravariant=True)
Rhs = TypeVar("Rhs", contravariant=True)
Result = TypeVar("Result", covariant=True)


# Math
class SupportsAdd(Protocol[Rhs, Result]):
    def __add__(self, other: Rhs) -> Result: ...


class SupportsSub(Protocol[Rhs, Result]):
    def __sub__(self, other: Rhs) -> Result: ...


class SupportsMul(Protocol[Rhs, Result]):
    def __mul__(self, other: Rhs) -> Result: ...


class SupportsPower(Protocol[Rhs, Result]):
    def __pow__(self, other: Rhs) -> Result: ...


class SupportsMatmul(Protocol[Rhs, Result]):
    def __matmul__(self, other: Rhs) -> Result: ...


class SupportsTruediv(Protocol[Rhs, Result]):
    def __truediv__(self, other: Rhs) -> Result: ...


class SupportsFloordiv(Protocol[Rhs, Result]):
    def __floordiv__(self, other: Rhs) -> Result: ...


class SupportsMod(Protocol[Rhs, Result]):
    def __mod__(self, other: Rhs) -> Result: ...


class SupportsAbs(Protocol[Result]):
    def __abs__(self) -> Result: ...


class SupportsRound(Protocol[Result]):
    def __round__(self, n: int) -> Result: ...


class SupportsTrunc(Protocol[Result]):
    def __trunc__(self) -> Result: ...


# Reversed math
class SupportsReverseAdd(Protocol[Lhs, Result]):
    def __radd__(self, other: Lhs) -> Result: ...


class SupportsReverseSub(Protocol[Rhs, Result]):
    def __rsub__(self, other: Rhs) -> Result: ...


class SupportsReverseMul(Protocol[Rhs, Result]):
    def __rmul__(self, other: Rhs) -> Result: ...


class SupportsReversePower(Protocol[Rhs, Result]):
    def __rpow__(self, other: Rhs) -> Result: ...


class SupportsReverseMatmul(Protocol[Rhs, Result]):
    def __rmatmul__(self, other: Rhs) -> Result: ...


class SupportsReverseTruediv(Protocol[Rhs, Result]):
    def __rtruediv__(self, other: Rhs) -> Result: ...


class SupportsReverseFloordiv(Protocol[Rhs, Result]):
    def __rfloordiv__(self, other: Rhs) -> Result: ...


class SupportsReverseMod(Protocol[Rhs, Result]):
    def __rmod__(self, other: Rhs) -> Result: ...


# Bitwise/boolean operators
class SupportsAnd(Protocol[Rhs, Result]):
    def __and__(self, other: Rhs) -> Result: ...


class SupportsOr(Protocol[Rhs, Result]):
    def __or__(self, other: Rhs) -> Result: ...


class SupportsXor(Protocol[Rhs, Result]):
    def __xor__(self, other: Rhs) -> Result: ...


class SupportsLShift(Protocol[Rhs, Result]):
    def __lshift__(self, other: Rhs) -> Result: ...


class SupportsRShift(Protocol[Rhs, Result]):
    def __rshift__(self, other: Rhs) -> Result: ...


class SupportsReverseAnd(Protocol[Rhs, Result]):
    def __rand__(self, other: Rhs) -> Result: ...


class SupportsReverseOr(Protocol[Rhs, Result]):
    def __ror__(self, other: Rhs) -> Result: ...


class SupportsReverseXor(Protocol[Rhs, Result]):
    def __rxor__(self, other: Rhs) -> Result: ...


class SupportsReverseLShift(Protocol[Rhs, Result]):
    def __rlshift__(self, other: Rhs) -> Result: ...


class SupportsReverseRShift(Protocol[Rhs, Result]):
    def __rrshift__(self, other: Rhs) -> Result: ...
