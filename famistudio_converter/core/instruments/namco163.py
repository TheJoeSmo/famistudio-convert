from attr import attrs

from ..expansion import Expansion
from .instrument import Instrument
from .wave_type import WaveType


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Namco163Instrument(Instrument):
    __expansion__ = Expansion.NAMCO

    wave: WaveType
    wave_size: int
    wave_position: int
    wave_count: int
