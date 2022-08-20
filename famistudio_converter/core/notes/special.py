from ._core import literal_property
from .note import Note
from .types import SpecialNoteType


class StopNote(Note):
    type = literal_property(SpecialNoteType.STOP)
    value = literal_property(0)
    duration = literal_property(1)

    __slots__ = ()


class ReleaseNote(Note):
    type = literal_property(SpecialNoteType.RELEASE)
    value = literal_property(0x80)
    duration = literal_property(1)

    __slots__ = ()
