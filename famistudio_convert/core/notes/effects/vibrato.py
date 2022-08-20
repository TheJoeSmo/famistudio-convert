from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class VibratoEffect(Effect):
    __user_names__ = ("Volume",)

    speed: int
    depth: int

    @property
    def value(self) -> int:
        return (self.speed << 4) + self.depth
