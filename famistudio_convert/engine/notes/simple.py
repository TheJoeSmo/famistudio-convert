from typing import ClassVar

from attr import attrs

from .types import MusicalNoteType


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class SimpleNote:
    NOTES_PER_OCTAVE: ClassVar[int] = 12

    octave: int
    type: MusicalNoteType

    @property
    def value(self) -> int:
        return self.octave * self.NOTES_PER_OCTAVE + self.type + 1

    @classmethod
    def from_value(cls, value: int):
        return cls(value // cls.NOTES_PER_OCTAVE, MusicalNoteType(value % cls.NOTES_PER_OCTAVE))
