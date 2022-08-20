from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class DutyCycleEffect(Effect):
    __user_names__ = ("DutyCycle",)

    duty: int
