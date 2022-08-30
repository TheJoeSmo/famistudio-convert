from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class DutyCycleEffect(Effect):
    __instrument_type__ = "DutyCycle"

    duty: int
