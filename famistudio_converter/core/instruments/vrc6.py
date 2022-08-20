from attr import attrs

from ..expansion import Expansion
from .instrument import Instrument


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class VRC6Instrument(Instrument):
    __expansion__ = Expansion.VRC6

    master_volume: int
