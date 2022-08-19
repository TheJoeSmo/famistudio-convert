from attr import attrs

from ..expansion import Expansion
from .instrument import Instrument


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class ExpandedPortSoundModuleInstrument(Instrument):
    __expansion__ = Expansion.EPSM

    master_volume: int
    patch: int
    patch_registers: list[int]
