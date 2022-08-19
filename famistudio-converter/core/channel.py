from enum import Enum, auto

from attr import attrs


class ChannelType(Enum):
    SQUARE1 = auto()
    SQUARE2 = auto()
    TRIANGLE = auto()
    NOISE = auto()
    DPCM = auto()
    VRC6SQUARE1 = auto()
    VRC6SQUARE2 = auto()
    VRC6SAW = auto()
    VRC7FM1 = auto()
    VRC7FM2 = auto()
    VRC7FM3 = auto()
    VRC7FM4 = auto()
    VRC7FM5 = auto()
    VRC7FM6 = auto()
    FDSWAVE = auto()
    MMC5SQUARE1 = auto()
    MMC5SQUARE2 = auto()
    MMC5DPCM = auto()
    N163WAVE1 = auto()
    N163WAVE2 = auto()
    N163WAVE3 = auto()
    N163WAVE4 = auto()
    N163WAVE5 = auto()
    N163WAVE6 = auto()
    N163WAVE7 = auto()
    N163WAVE8 = auto()
    S5BSQUARE1 = auto()
    S5BSQUARE2 = auto()
    S5BSQUARE3 = auto()
    EPSMSQUARE1 = auto()
    EPSMSQUARE2 = auto()
    EPSMSQUARE3 = auto()
    EPSMFM1 = auto()
    EPSMFM2 = auto()
    EPSMFM3 = auto()
    EPSMFM4 = auto()
    EPSMFM5 = auto()
    EPSMFM6 = auto()
    EPSMRYTHM1 = auto()
    EPSMRYTHM2 = auto()
    EPSMRYTHM3 = auto()
    EPSMRYTHM4 = auto()
    EPSMRYTHM5 = auto()
    EPSMRYTHM6 = auto()


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Channel:
    type: ChannelType