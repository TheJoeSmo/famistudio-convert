from attr import attrs

from ..conversion import Attribute
from .notes import PrimitiveMusicalNote


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Sample(Attribute):
    title: str
    data: bytearray


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class _SampleNote:
    sample: Sample
    pitch: int
    loop: bool
    initial_value: int


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class SampleNote(Attribute, _SampleNote):
    index: int

    @property
    def note(self) -> PrimitiveMusicalNote:
        return PrimitiveMusicalNote.from_value(self.index)
