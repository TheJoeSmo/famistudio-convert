from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class DeltaCounterEffect(Effect):
    __user_names__ = ("DeltaCounter",)

    delta: int
