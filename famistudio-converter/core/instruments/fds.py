from attr import attrs

from ..expansion import Expansion
from .instrument import Instrument
from .wave_type import WaveType


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class FamilyDiskSystemInstrument(Instrument):
    __expansion__ = Expansion.FDS

    wave: WaveType
    modulator: WaveType
    master_volume: int
    modulation_speed: int
    modulation_depth: int
    modulation_delay: int
