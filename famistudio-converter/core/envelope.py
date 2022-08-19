from enum import Enum, auto


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


class Envelope:
    type: EnvelopeType
    loop: int | None
    release: int | None
    is_relative: bool
    values: list[int]
