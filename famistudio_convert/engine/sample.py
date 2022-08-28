from collections.abc import Mapping

from attr import attrs

from ..conversion import Attribute


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Sample(Attribute):
    title: str
    data: bytearray


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class SampleNote(Attribute):
    title: str
    pitch: int
    loop: bool
    initial_value: int


SampleMap = Mapping[int, SampleNote]
