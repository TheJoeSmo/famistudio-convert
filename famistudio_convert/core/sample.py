from collections.abc import Mapping

from attr import attrs


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Sample:
    title: str
    data: bytearray


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class SampleNote:
    title: str
    pitch: int
    loop: bool
    initial_value: int


SampleMap = Mapping[int, SampleNote]
