from attr import attrs

from .envelope import Envelope


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Arpeggio:
    title: str
    length: int
    loop: int
    envelope: Envelope
