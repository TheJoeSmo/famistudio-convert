from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class DeltaCounterEffect(Effect):
    __instrument_type__ = "DeltaCounter"

    delta: int
