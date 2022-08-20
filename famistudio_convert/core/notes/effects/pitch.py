from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class PitchEffect(Effect):
    __user_names__ = ("FinePitch",)

    pitch: int
