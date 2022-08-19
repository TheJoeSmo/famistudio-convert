from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class VolumeEffect(Effect):
    __user_names__ = ("Volume",)

    volume: int


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class VolumeSlideEffect(Effect):
    __user_names__ = ("VolumeSlideTarget",)

    volume: int
