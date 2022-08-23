from typing import Generic, TypeVar

from attr import attrs

from ..types import ConversionTypes

_T = TypeVar("_T")


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Field(Generic[_T]):
    title: str
    value: _T

    def generate(self, type: ConversionTypes) -> tuple[str]:
        ...
