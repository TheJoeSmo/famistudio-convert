from __future__ import annotations

from abc import ABC, abstractmethod
from re import Match, search
from typing import ClassVar, Generic, TypeVar

from attr import attrs

from ..core import is_none, is_type, maybe
from ..logging import log

_T = TypeVar("_T")
_new_line_char = "\n"


@attrs(slots=True, auto_attribs=True)
class InvalidPatternException(ValueError):
    message: str


@attrs(slots=True, auto_attribs=True)
class Handler(Generic[_T], ABC):
    def __call__(self, obj: _T, found: str) -> str:
        return self.solve(obj, found)

    @classmethod
    @abstractmethod
    def solve(cls, obj: _T, found: str) -> str:
        ...


@attrs(slots=True, auto_attribs=True)
class GreedyHandler(Handler[_T]):
    __patterns__: ClassVar[tuple[Pattern, ...]]

    @classmethod
    def solve(cls, obj: _T, found: str) -> str:
        log.info(f"{cls.__name__} solving {found} for {obj}")
        for pattern in cls.__patterns__:
            found = pattern.solve(obj, found)
        return found


@attrs(slots=True, auto_attribs=True, eq=True)
class Pattern(Generic[_T]):
    pattern: str | None
    handler: Handler[_T]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.handler.__class__.__name__}, {self.pattern}]"

    def find_match(self, string: str) -> str | None:
        result = maybe(
            lambda: is_type(Match)(search(self.pattern, string), lambda m: m.group(1)),  # type: ignore
            start=is_none(self.pattern, string),
        )
        if result is None:
            log.info(
                f"{self!s} did not find match with pattern '{self.pattern}' "
                + f"from string {string.split(_new_line_char)}."
            )
        else:
            log.info(
                f"{self!s} found {result.split(_new_line_char)} with pattern '{self.pattern}' "
                + f"from string {string.split(_new_line_char)}."
            )
        return result

    def solve_match(self, cls: _T, found: str, *args, **kwargs) -> str:
        result = self.handler(cls, found, *args, **kwargs)
        log.info(
            f"{self!s} provided solved {result.split(_new_line_char)} from "
            + f"{found.split(_new_line_char)} with {cls.__class__.__name__}, {args} and {kwargs}"
        )
        return result

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
        result = string.replace(found, solved_match, 1)
        log.info(
            f"{self!s} provided {solved_match.split(_new_line_char)} from {found.split(_new_line_char)} "
            + f"with {cls.__class__.__name__}, {args}, and {kwargs} resulting into {result.split(_new_line_char)}"
        )
        return result

    def solve(self, cls: _T, string: str, *args, **kwargs) -> str:
        log.info(
            f"{self!s} solving {string.split(_new_line_char)} for " + f"{cls.__class__.__name__}, {args}, and {kwargs}"
        )
        while found := self.find_match(string):
            past_string = string
            string = self.solve_and_replace_next_match(cls, string, found, *args, **kwargs)
            assert past_string != string

        log.info(f"{self!s} solved result is {string.split(_new_line_char)}")
        return string
