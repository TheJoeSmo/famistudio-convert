from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class AttackEffect(Effect):
    __instrument_type__ = "Attack"

    has_attack: bool
