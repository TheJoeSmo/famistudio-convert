from attr import attrs

from .effect import Effect


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class NoteDelayEffect(Effect):
    __user_names__ = ("NoteDelay",)

    delay: int


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class NoteCutEffect(Effect):
    __user_names__ = ("NoteCut",)

    delay: int
