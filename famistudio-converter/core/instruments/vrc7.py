from attr import attrs

from ..expansion import Expansion
from .instrument import Instrument

VRC7PatchRegisters = tuple[int, int, int, int, int, int, int, int]


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class VRC7Instrument(Instrument):
    __expansion__ = Expansion.VRC7

    patch: int
    patch_registers: VRC7PatchRegisters
