from collections.abc import Sequence

from attr import attrs

from ..arpeggio import Arpeggio
from ..instruments import Instrument
from .effects import Effect
from .note import Note
from .simple import SimpleNote
from .types import MusicalNoteType


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class MusicalNote(Note):
    note: SimpleNote
    duration_: int
    release_: int | None
    instrument_: Instrument
    arpeggio_: Arpeggio
    slide_note: SimpleNote
    effects: Sequence[Effect]

    @property
    def type(self) -> MusicalNoteType:
        return self.note.type

    @property
    def octave(self) -> int:
        return self.note.octave

    @property
    def value(self) -> int:
        return self.note.value

    @property
    def duration(self) -> int:
        return self.duration_

    @property
    def release(self) -> int | None:
        return self.release_

    @property
    def instrument(self) -> Instrument:
        return self.instrument_

    @property
    def arpeggio(self) -> Arpeggio:
        return self.arpeggio_

    @property
    def slide_target(self) -> int:
        return self.slide_note.value
