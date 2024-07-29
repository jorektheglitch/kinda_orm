from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Callable, ClassVar, Generic, Mapping, ParamSpec, Type, TypeVar, overload
from typing import cast as _cast

from kinda_orm.protocols import (
    SupportsAbs, SupportsAdd, SupportsAnd, SupportsDivmod, SupportsFloordiv, SupportsInvert, SupportsLShift,
    SupportsMatmul, SupportsMod, SupportsMul, SupportsNeg, SupportsOr, SupportsPos, SupportsPower, SupportsRShift,
    SupportsRound, SupportsSub, SupportsTruediv, SupportsTrunc, SupportsXor,
)
from kinda_orm.protocols import (
    SupportsReverseAdd, SupportsReverseAnd, SupportsReverseDivmod, SupportsReverseFloordiv, SupportsReverseLShift,
    SupportsReverseMatmul, SupportsReverseMod, SupportsReverseMul, SupportsReverseOr, SupportsReversePower,
    SupportsReverseRShift, SupportsReverseSub, SupportsReverseTruediv, SupportsReverseXor,
)
from kinda_orm.protocols import (
    SupportsEquals, SupportsLessOrEquals,
    SupportsGreaterOrEquals, SupportsGreaterThan,
    SupportsLessThan, SupportsNotEquals
)
from kinda_orm.protocols import Indexable, Sliceable
from kinda_orm.protocols import Lhs, Rhs, Result
from kinda_orm.protocols import Index, Item


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

Params = ParamSpec("Params")
Return = TypeVar("Return", covariant=True)


class UnaryOperator(StrEnum):
    pos = '+'
    neg = '-'
    invert = '~'

    @property
    def priority(self) -> int:
        return _OPERATORS_PRIORITIES[self]


class BinOperator(StrEnum):
    add = '+'
    sub = '-'
    mul = "*"
    pow = '**'
    matmul = '@'
    truediv = '/'
    floordiv = '//'
    mod = '%'
    and_ = '&'
    or_ = '|'
    xor = '^'
    lshift = '<<'
    rshift = '>>'
    eq = '=='
    ne = '!='
    lt = '<'
    le = '<='
    ge = '>='
    gt = '>'

    @property
    def priority(self) -> int:
        return _OPERATORS_PRIORITIES[self]


_OPERATORS_PRIORITIES: Mapping[BinOperator | UnaryOperator, int] = {
    BinOperator.pow: 8,
    UnaryOperator.pos: 7,
    UnaryOperator.neg: 7,
    UnaryOperator.invert: 7,
    BinOperator.mul: 6,
    BinOperator.matmul: 6,
    BinOperator.truediv: 6,
    BinOperator.floordiv: 6,
    BinOperator.mod: 6,
    BinOperator.add: 5,
    BinOperator.sub: 5,
    BinOperator.lshift: 4,
    BinOperator.rshift: 4,
    BinOperator.and_: 3,
    BinOperator.xor: 2,
    BinOperator.or_: 1,
    BinOperator.eq: 0,
    BinOperator.ne: 0,
    BinOperator.lt: 0,
    BinOperator.le: 0,
    BinOperator.ge: 0,
    BinOperator.gt: 0,
}


@dataclass
class Expr(Generic[T_co]):

    # Math operations

    def __abs__(self: Expr[SupportsAbs[Result]]) -> AbsExpr[Result]:
        return AbsExpr(self)

    def __round__(self: Expr[SupportsRound[Result]], n: int) -> RoundExpr[Result]:
        return RoundExpr(self, n)

    def __trunc__(self: Expr[SupportsTrunc[Result]]) -> Expr[Result]:
        return TruncExpr(self)

    def __divmod__(self: Expr[SupportsDivmod[Rhs, Result]],
                   other: Expr[Rhs] | Rhs,
                   ) -> Expr[Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return DivmodExpr(self, other)

    def __pos__(self: Expr[SupportsPos[Result]]) -> Expr[Result]:
        return PosExpr(self)

    def __neg__(self: Expr[SupportsNeg[Result]]) -> Expr[Result]:
        return NegExpr(self)

    def __invert__(self: Expr[SupportsInvert[Result]]) -> Expr[Result]:
        return InvertExpr(self)

    def __add__(self: Expr[SupportsAdd[Rhs, Result]],
                other: Expr[Rhs] | Rhs
                ) -> AddExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return AddExpr(self, other)

    def __sub__(self: Expr[SupportsSub[Rhs, Result]],
                other: Expr[Rhs] | Rhs
                ) -> SubExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return SubExpr(self, other)

    def __mul__(self: Expr[SupportsMul[Rhs, Result]],
                other: Expr[Rhs] | Rhs
                ) -> MulExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return MulExpr(self, other)

    def __pow__(self: Expr[SupportsPower[Rhs, Result]],
                other: Expr[Rhs] | Rhs
                ) -> PowerExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return PowerExpr(self, other)

    def __matmul__(self: Expr[SupportsMatmul[Rhs, Result]],
                   other: Expr[Rhs] | Rhs
                   ) -> MatmulExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return MatmulExpr(self, other)

    def __truediv__(self: Expr[SupportsTruediv[Rhs, Result]],
                    other: Expr[Rhs] | Rhs
                    ) -> TruedivExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return TruedivExpr(self, other)

    def __floordiv__(self: Expr[SupportsFloordiv],
                     other: Expr[Rhs] | Rhs
                     ) -> FloordivExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return FloordivExpr(self, other)

    def __mod__(self: Expr[SupportsMod[Rhs, Result]],
                other: Expr[Rhs] | Rhs
                ) -> ModExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ModExpr(self, other)

    def __and__(self: Expr[SupportsAnd[Rhs, Result]],
                other: Expr[Rhs] | Rhs
                ) -> AndExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return AndExpr(self, other)

    def __or__(self: Expr[SupportsOr[Rhs, Result]],
               other: Expr[Rhs] | Rhs
               ) -> OrExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return OrExpr(self, other)

    def __xor__(self: Expr[SupportsXor[Rhs, Result]],
                other: Expr[Rhs] | Rhs
                ) -> XorExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return XorExpr(self, other)

    def __lshift__(self: Expr[SupportsLShift[Rhs, Result]],
                   other: Expr[Rhs] | Rhs
                   ) -> LShiftExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return LShiftExpr(self, other)

    def __rshift__(self: Expr[SupportsRShift[Rhs, Result]],
                   other: Expr[Rhs] | Rhs
                   ) -> RShiftExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return RShiftExpr(self, other)

    # Reversed math operations

    def __rdivmod__(self: Expr[SupportsReverseDivmod[Lhs, Result]],
                    other: Expr[Lhs] | Lhs
                    ) -> ReverseDivmodExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseDivmodExpr(other, self)

    def __radd__(self: Expr[SupportsReverseAdd[Lhs, Result]],
                 other: Expr[Lhs] | Lhs,
                 ) -> ReverseAddExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseAddExpr(other, self)

    def __rsub__(self: Expr[SupportsReverseSub[Lhs, Result]],
                 other: Expr[Lhs] | Lhs
                 ) -> ReverseSubExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseSubExpr(other, self)

    def __rpow__(self: Expr[SupportsReversePower[Lhs, Result]],
                 other: Expr[Lhs] | Lhs
                 ) -> ReversePowerExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReversePowerExpr(other, self)

    def __rmatmul__(self: Expr[SupportsReverseMatmul[Lhs, Result]],
                    other: Expr[Lhs] | Lhs
                    ) -> ReverseMatmulExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseMatmulExpr(other, self)

    def __rtruediv__(self: Expr[SupportsReverseTruediv[Lhs, Result]],
                     other: Expr[Lhs] | Lhs
                     ) -> ReverseTruedivExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseTruedivExpr(other, self)

    def __rfloordiv__(self: Expr[SupportsReverseFloordiv[Lhs, Result]],
                      other: Expr[Lhs] | Lhs
                      ) -> ReverseFloordivExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseFloordivExpr(other, self)

    def __rmod__(self: Expr[SupportsReverseMod[Lhs, Result]],
                 other: Expr[Lhs] | Lhs
                 ) -> ReverseModExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseModExpr(other, self)

    def __rand__(self: Expr[SupportsReverseAnd[Lhs, Result]],
                 other: Expr[Lhs] | Lhs
                 ) -> ReverseAndExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseAndExpr(other, self)

    def __ror__(self: Expr[SupportsReverseOr[Lhs, Result]],
                other: Expr[Lhs] | Lhs
                ) -> ReverseOrExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseOrExpr(other, self)

    def __rxor__(self: Expr[SupportsReverseXor[Lhs, Result]],
                 other: Expr[Lhs] | Lhs
                 ) -> ReverseXorExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseXorExpr(other, self)

    def __rlshift__(self: Expr[SupportsReverseLShift[Lhs, Result]],
                    other: Expr[Lhs] | Lhs
                    ) -> ReverseLShiftExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseLShiftExpr(other, self)

    def __rrshift__(self: Expr[SupportsReverseRShift[Lhs, Result]],
                    other: Expr[Lhs] | Lhs
                    ) -> ReverseRShiftExpr[Lhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return ReverseRShiftExpr(other, self)

    # Comparisons

    def __eq__(self: Expr[SupportsEquals[Rhs, Result]],  # type: ignore
               other: Expr[Rhs] | Rhs
               ) -> EqualExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return EqualExpr(self, other)

    def __ne__(self: Expr[SupportsNotEquals[Rhs, Result]],  # type: ignore
               other: Expr[Rhs] | Rhs
               ) -> NotEqualExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return NotEqualExpr(self, other)

    def __lt__(self: Expr[SupportsLessThan[Rhs, Result]],
               other: Expr[Rhs] | Rhs
               ) -> LessThanExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return LessThanExpr(self, other)

    def __le__(self: Expr[SupportsLessOrEquals[Rhs, Result]],
               other: Expr[Rhs] | Rhs
               ) -> LessOrEqualExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return LessOrEqualExpr(self, other)

    def __ge__(self: Expr[SupportsGreaterOrEquals[Rhs, Result]],
               other: Expr[Rhs] | Rhs
               ) -> GreaterOrEqualExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return GreaterOrEqualExpr(self, other)

    def __gt__(self: Expr[SupportsGreaterThan[Rhs, Result]],
               other: Expr[Rhs] | Rhs
               ) -> GreaterThanExpr[Rhs, Result]:
        if not isinstance(other, Expr):
            other = ConstExpr(other)
        return GreaterThanExpr(self, other)

    # Some other stuff

    @overload
    # NOTE: here two overloads overlaps with different types, but it seems OK
    def __getitem__(self: Expr[Sliceable[Item]],  # type: ignore
                    index: slice
                    ) -> GetSliceExpr[Item]: ...

    @overload
    def __getitem__(self: Expr[Indexable[Index, Item]],
                    index: Expr[Index] | Index
                    ) -> GetItemExpr[Index, Item]: ...

    def __getitem__(self: Expr[Indexable[Index, Item]] | Expr[Sliceable[Item]],
                    index: Expr[Index] | Index | slice
                    ) -> GetItemExpr[Index, Item] | GetSliceExpr[Item]:
        if isinstance(index, slice):
            self = _cast(Expr[Sliceable[Item]], self)
            return GetSliceExpr(self, index)
        self = _cast(Expr[Indexable[Index, Item]], self)
        return GetItemExpr(self, index)

    def __getattr__(self,
                    name: str) -> Any | Expr[Any]:
        if not name.startswith('_'):
            return GetAttrExpr(self, name)
        return super().__getattribute__(name)

    def __call__(self: Expr[Callable[Params, Result]],
                 *args: Params.args,
                 **kwargs: Params.kwargs) -> CallExpr[Params, Result]:
        return CallExpr(self, args, kwargs)


@dataclass(eq=False)
class ConstExpr(Expr[T_co]):
    value: T_co

    def __str__(self) -> str:
        return repr(self.value)


@dataclass(init=False, eq=False)
class Variable(Expr[T_co]):
    name: str
    type: Type[T_co] | None = None

    @overload
    def __init__(self: Variable[T_co], *, name: str, type: Type[T_co]) -> None: ...
    @overload
    def __init__(self: Variable[Any], *, name: str, type: None = None) -> None: ...

    def __init__(self: Variable[Any], *, name: str, type: Type[T_co] | None = None) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        type_spec = f" of type {repr(self.type)}" if self.type else ""
        return f"<{self.name}{type_spec}>"


@dataclass
class PyFunction(Expr[Callable[Params, Return]], Generic[Params, Return]):
    fn: Callable[Params, Return]


@dataclass
class CastExpr(Expr[Result]):
    expr: Expr[Any]
    type: type[Result]


@dataclass
class AbsExpr(Expr[Result]):
    arg: Expr[SupportsAbs[Result]]


@dataclass
class DivmodExpr(Expr[Result], Generic[Rhs, Result]):
    left: Expr[SupportsDivmod[Rhs, Result]]
    right: Expr[Rhs]


@dataclass
class ReverseDivmodExpr(Expr[Result], Generic[Lhs, Result]):
    left: Expr[Lhs]
    right: Expr[SupportsReverseDivmod[Lhs, Result]]


@dataclass
class RoundExpr(Expr[Result]):
    arg: Expr[SupportsRound[Result]]
    precision: int


@dataclass
class TruncExpr(Expr[Result]):
    arg: Expr[SupportsTrunc[Result]]


@dataclass
class UnaryExpr(Expr[Result], Generic[Rhs, Result]):
    arg: Expr[Rhs]
    operator: ClassVar[UnaryOperator]

    def __str__(self) -> str:
        return f"{self.operator}{self.arg}"


@dataclass
class PosExpr(UnaryExpr[SupportsPos[Result], Result]):
    operator = UnaryOperator.pos


@dataclass
class NegExpr(UnaryExpr[SupportsNeg[Result], Result]):
    operator = UnaryOperator.neg


@dataclass
class InvertExpr(UnaryExpr[SupportsInvert[Result], Result]):
    operator = UnaryOperator.invert


@dataclass
class BinExpr(Expr[Result], Generic[Lhs, Rhs, Result]):
    left: Expr[Lhs]
    right: Expr[Rhs]
    operator: ClassVar[BinOperator]

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"


@dataclass
class AddExpr(BinExpr[SupportsAdd[Rhs, Result], Rhs, Result]):
    operator = BinOperator.add


@dataclass
class SubExpr(BinExpr[SupportsSub[Rhs, Result], Rhs, Result]):
    operator = BinOperator.sub


@dataclass
class MulExpr(BinExpr[SupportsMul[Rhs, Result], Rhs, Result]):
    operator = BinOperator.mul


@dataclass
class PowerExpr(BinExpr[SupportsPower[Rhs, Result], Rhs, Result]):
    operator = BinOperator.pow


@dataclass
class MatmulExpr(BinExpr[SupportsMatmul[Rhs, Result], Rhs, Result]):
    operator = BinOperator.matmul


@dataclass
class TruedivExpr(BinExpr[SupportsTruediv[Rhs, Result], Rhs, Result]):
    operator = BinOperator.truediv


@dataclass
class FloordivExpr(BinExpr[SupportsFloordiv[Rhs, Result], Rhs, Result]):
    operator = BinOperator.floordiv


@dataclass
class ModExpr(BinExpr[SupportsMod[Rhs, Result], Rhs, Result]):
    operator = BinOperator.mod


@dataclass
class AndExpr(BinExpr[SupportsAnd[Rhs, Result], Rhs, Result]):
    operator = BinOperator.and_


@dataclass
class OrExpr(BinExpr[SupportsOr[Rhs, Result], Rhs, Result]):
    operator = BinOperator.or_


@dataclass
class XorExpr(BinExpr[SupportsXor[Rhs, Result], Rhs, Result]):
    operator = BinOperator.xor


@dataclass
class LShiftExpr(BinExpr[SupportsLShift[Rhs, Result], Rhs, Result]):
    operator = BinOperator.lshift


@dataclass
class RShiftExpr(BinExpr[SupportsRShift[Rhs, Result], Rhs, Result]):
    operator = BinOperator.rshift


@dataclass
class ReverseAddExpr(BinExpr[Lhs, SupportsReverseAdd[Lhs, Result], Result]):
    operator = BinOperator.add


@dataclass
class ReverseSubExpr(BinExpr[Lhs, SupportsReverseSub[Lhs, Result], Result]):
    operator = BinOperator.sub


@dataclass
class ReverseMulExpr(BinExpr[Lhs, SupportsReverseMul[Lhs, Result], Result]):
    operator = BinOperator.mul


@dataclass
class ReversePowerExpr(BinExpr[Lhs, SupportsReversePower[Lhs, Result], Result]):
    operator = BinOperator.pow


@dataclass
class ReverseMatmulExpr(BinExpr[Lhs, SupportsReverseMatmul[Lhs, Result], Result]):
    operator = BinOperator.matmul


@dataclass
class ReverseTruedivExpr(BinExpr[Lhs, SupportsReverseTruediv[Lhs, Result], Result]):
    operator = BinOperator.truediv


@dataclass
class ReverseFloordivExpr(BinExpr[Lhs, SupportsReverseFloordiv[Lhs, Result], Result]):
    operator = BinOperator.floordiv


@dataclass
class ReverseModExpr(BinExpr[Lhs, SupportsReverseMod[Lhs, Result], Result]):
    operator = BinOperator.mod


@dataclass
class ReverseAndExpr(BinExpr[Lhs, SupportsReverseAnd[Lhs, Result], Result]):
    operator = BinOperator.and_


@dataclass
class ReverseOrExpr(BinExpr[Lhs, SupportsReverseOr[Lhs, Result], Result]):
    operator = BinOperator.or_


@dataclass
class ReverseXorExpr(BinExpr[Lhs, SupportsReverseXor[Lhs, Result], Result]):
    operator = BinOperator.xor


@dataclass
class ReverseLShiftExpr(BinExpr[Lhs, SupportsReverseLShift[Lhs, Result], Result]):
    operator = BinOperator.lshift


@dataclass
class ReverseRShiftExpr(BinExpr[Lhs, SupportsReverseRShift[Lhs, Result], Result]):
    operator = BinOperator.rshift


@dataclass
class EqualExpr(BinExpr[SupportsEquals[Rhs, Result], Rhs, Result]):
    operator = BinOperator.eq


@dataclass
class NotEqualExpr(BinExpr[SupportsNotEquals[Rhs, Result], Rhs, Result]):
    operator = BinOperator.ne


@dataclass
class LessThanExpr(BinExpr[SupportsLessThan[Rhs, Result], Rhs, Result]):
    operator = BinOperator.lt


@dataclass
class LessOrEqualExpr(BinExpr[SupportsLessOrEquals[Rhs, Result], Rhs, Result]):
    operator = BinOperator.le


@dataclass
class GreaterOrEqualExpr(BinExpr[SupportsGreaterOrEquals[Rhs, Result], Rhs, Result]):
    operator = BinOperator.ge


@dataclass
class GreaterThanExpr(BinExpr[SupportsGreaterThan[Rhs, Result], Rhs, Result]):
    operator = BinOperator.gt


@dataclass
class GetItemExpr(Expr[Item], Generic[Index, Item]):
    sequence: Expr[Indexable[Index, Item]]
    index: Index | Expr[Index]

    def __str__(self) -> str:
        return f"{self.sequence}[{self.index}]"


@dataclass
class GetSliceExpr(Expr[Item], Generic[Item]):
    sequence: Expr[Sliceable[Item]]
    index: slice

    def __str__(self) -> str:
        indices = self.index.start, self.index.stop, self.index.step
        if indices == (None, None, None):
            slice_spec: str = ":"
        elif indices[2] is None:
            slice_spec = ":".join(idc if idc is not None else '' for idc in indices[:2])
        else:
            slice_spec = ":".join(idc if idc is not None else '' for idc in indices)
        return f"{self.sequence}[{slice_spec}]"


@dataclass
class GetAttrExpr(Expr[Result], Generic[Lhs, Result]):
    obj: Expr[Lhs]
    name: str


@dataclass
class CallExpr(Expr[Return], Generic[Params, Return]):
    fn: Expr[Callable[Params, Return]]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

    def __str__(self) -> str:
        args_spec = ", ".join(map(repr, self.args))
        kwds_spec = ", ".join(f"{name}={repr(value)}" for name, value in self.kwargs.items())
        full_spec = ", ".join(filter(None, (args_spec, kwds_spec)))
        return f"{self.fn}({full_spec})"


def cast(expr: Expr[Any], type: type[Result]) -> CastExpr[Result]:
    return CastExpr(expr, type)
