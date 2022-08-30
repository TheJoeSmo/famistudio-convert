from collections.abc import Sequence

from attr import attrs

from ..conversion import Attribute
from .arpeggio import Arpeggio
from .expansion import Expansion
from .instruments import Instrument
from .sample import Sample, SampleNote
from .song import FamistudioPattern, Song


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Project(Attribute):
    title: str
    author: str
    copyright: str
    version: str
    is_pal: bool
    expansions: Sequence[Expansion]
    samples: Sequence[Sample]
    sample_map: Sequence[SampleNote]
    instruments: Sequence[Instrument]
    arpeggios: Sequence[Arpeggio]
    songs: Sequence[Song]

    @property
    def type(self) -> str:
        return "Famistudio" if isinstance(self.songs[0].default_pattern, FamistudioPattern) else "FamiTracker"
