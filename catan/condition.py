from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
import numpy.typing as npt
from typing import Any, Optional, Callable, Protocol


@dataclass
class ConditionKeeper:
    status_memo: dict[str, bool | npt.NDArray[bool]] = field(init=False)

    def __post_init__(self):
        self.status_memo = {}

    def get_status(self, condition: Condition) -> bool | npt.NDArray[bool]:
        if condition.identifier in self.status_memo:
            return self.status_memo[condition.identifier]

        self.status_memo[condition.identifier] = condition.check(self)
        print(f'{condition.identifier}: {self.status_memo[condition.identifier]}')
        return self.status_memo[condition.identifier].copy()


@dataclass
class Condition:
    value: Optional[int] = field(kw_only=True, default=None)

    @property
    def identifier(self) -> str:
        if self.value is None:
            return self.__class__.__name__
        return f'{self.__class__.__name__}_{self.value}'

    def get_status(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
        return keeper.get_status(self)

    def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
        ...

    def __and__(*conditions) -> LogicalAndCondition:
        return LogicalAndCondition(conditions=list(conditions))

    def __or__(*conditions) -> LogicalOrCondition:
        return LogicalOrCondition(conditions=list(conditions))

    def __invert__(self) -> InvertCondition:
        return InvertCondition(cond=self)


@dataclass
class AnyTrue(Condition):
    condition: Condition = field(default=None)

    @property
    def identifier(self) -> str:
        return f'any_{self.condition.identifier}'

    def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
        return np.any(self.condition.check(keeper))


@dataclass
class LogicalAndCondition(Condition):
    conditions: list[Condition] = field(kw_only=True, default_factory=list)

    @property
    def identifier(self) -> str:
        return '&'.join(cond.identifier for cond in self.conditions)

    def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
        return np.logical_and.reduce([keeper.get_status(cond) for cond in self.conditions])


@dataclass
class LogicalOrCondition(Condition):
    conditions: list[Condition] = field(kw_only=True, default_factory=list)

    @property
    def identifier(self) -> str:
        return '|'.join(cond.identifier for cond in self.conditions)

    def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
        return np.logical_or.reduce([keeper.get_status(cond) for cond in self.conditions])


@dataclass
class InvertCondition(Condition):
    cond: Condition = field(kw_only=True, default=None)

    @property
    def identifier(self) -> str:
        return f'~{self.cond}'

    def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
        return np.invert(keeper.get_status(self.cond))


#
# @dataclass
# class TestA(Condition):
#     _tag = 'Test_A'
#     value: int = field(kw_only=True, default=None)
#
#     def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
#         return np.array([True, False, True, True], dtype=bool)
#
#
# @dataclass
# class TestB(Condition):
#     _tag = 'Test_B'
#     value: int = field(kw_only=True, default=1)
#
#     def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
#         return np.array([True, True, True, False], dtype=bool)
#
#
# @dataclass
# class TestC(Condition):
#     _tag = 'Test_C'
#     value: int = field(kw_only=True, default=1)
#
#     def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
#         return np.array([True, False, True, True], dtype=bool)
#
#
# @dataclass
# class TestD(Condition):
#     _tag = 'Test_D'
#     value: int = field(kw_only=True, default=1)
#
#     def check(self, keeper: ConditionKeeper) -> bool | npt.NDArray[bool]:
#         return np.array([False, True, False, True], dtype=bool)
#
