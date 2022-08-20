from enum import Enum, auto


class WaveType(Enum):
    SINE = auto()
    TRIANGLE = auto()
    SAW_TOOTH = auto()
    SQUARE_50 = auto()
    SQUARE_25 = auto()
    FLAT = auto()
    CUSTOM = auto()
    RESAMPLE = auto()
