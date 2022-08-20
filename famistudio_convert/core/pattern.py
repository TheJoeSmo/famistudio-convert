from collections.abc import Mapping

from attr import attrs

from .notes import Note


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Pattern:
    title: str
    notes: Mapping[int, Note]


PatternInstance = tuple[int, Pattern]
