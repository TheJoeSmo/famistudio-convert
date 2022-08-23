from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class FamistudioModulationSpeedEffect(Effect):
    __user_names__ = ("FdsModSpeed",)

    speed: int


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class FamistudioModulationDepthEffect(Effect):
    __user_names__ = ("FdsModDepth",)

    depth: int
