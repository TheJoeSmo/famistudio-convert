from enum import Enum, auto

from attr import attrs

from ..conversion import Attribute


class EnvelopeType(Enum):
    VOLUME = auto()
    ARPEGGIO = auto()
    PITCH = auto()
    DUTY_CYCLE = auto()
    REGULAR_COUNT = auto()
    FDS_WAVEFORM = auto()
    FDS_MODULATION = auto()
    NAMCO163_WAVEFORM = auto()
    WAVEFORM_REPEAT = auto()


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Envelope(Attribute):
    type: EnvelopeType
    loop: int | None
    release: int | None
    is_relative: bool
    values: list[int]