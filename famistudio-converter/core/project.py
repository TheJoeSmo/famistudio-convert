from collections.abc import Sequence

from attr import attrs

from .arpeggio import Arpeggio
from .channel import Channel
from .expansion import Expansion
from .instruments import Instrument
from .sample import Sample, SampleMap


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Project:
    title: str
    author: str
    copyright: str
    is_pal: bool
    expansions: Sequence[Expansion]
    samples: Sequence[Sample]
    sample_map: SampleMap
    instruments: Sequence[Instrument]
    arpeggios: Sequence[Arpeggio]
    channels: Sequence[Channel]
