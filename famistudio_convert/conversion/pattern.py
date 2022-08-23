from __future__ import annotations

from abc import ABC, abstractmethod
from re import Match, search
from typing import ClassVar, Generic, TypeVar

from attr import attrs

from ..core import is_none, is_type, maybe

_T = TypeVar("_T")


class InvalidPatternException(ValueError):
    pass


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Handler(Generic[_T], ABC):
    def __call__(self, obj: _T, found: str) -> str:
        return self.solve(obj, found)

    @classmethod
    @abstractmethod
    def solve(cls, obj: _T, found: str) -> str:
        ...


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class GreedyHandler(Handler[_T]):
    __patterns__: ClassVar[tuple[Pattern]]

    @classmethod
    def solve(cls, obj: _T, found: str) -> str:
        for pattern in cls.__patterns__:
            found = pattern.solve(obj, found)
        return found


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Pattern(Generic[_T]):
    pattern: str | None
    handler: Handler[_T]

    def find_match(self, string: str) -> str | None:
        return maybe(
            lambda: is_type(Match)(search(self.pattern, string), lambda m: m.group(1)),  # type: ignore
            start=is_none(self.pattern, string),
        )

    def solve_match(self, cls: _T, found: str, *args, **kwargs) -> str:
        return self.handler(cls, found, *args, **kwargs)

    def solve_next_match(self, cls: _T, string: str, found: str | None = None, *args, **kwargs) -> str:
        return self.solve_match(
            cls,
            maybe(
                lambda: self.find_match(string),
                start=found,
                exception=lambda: LookupError(f" { self.pattern} found no matches inside {string}"),
            ),
            *args,
            **kwargs,
        )

    def solve_and_replace_next_match(self, cls: _T, string: str, found: str | None = None, *args, **kwargs) -> str:
        found = self.find_match(string) if found is None else found
        solved_match = self.solve_next_match(cls, string, found, *args, **kwargs)
        assert isinstance(found, str)  # impossible state
        return string.replace(found, solved_match, 1)

    def solve(self, cls: _T, string: str, *args, **kwargs) -> str:
        while found := self.find_match(string):
            string = self.solve_and_replace_next_match(cls, string, found, *args, **kwargs)
        return string
