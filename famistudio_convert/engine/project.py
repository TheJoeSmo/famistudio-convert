from collections.abc import Sequence

from attr import attrs

from .arpeggio import Arpeggio
from .expansion import Expansion
from .instruments import Instrument
from .sample import Sample, SampleMap
from .song import FamistudioPattern, Song


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Project:
    title: str
    author: str
    copyright: str
    version: str
    is_pal: bool
    expansions: Sequence[Expansion]
    samples: Sequence[Sample]
    sample_map: SampleMap
    instruments: Sequence[Instrument]
    arpeggios: Sequence[Arpeggio]
    songs: Sequence[Song]

    @property
    def type(self) -> str:
        return "Famistudio" if isinstance(self.songs[0].default_pattern, FamistudioPattern) else "FamiTracker"
