from .espm import ExpandedPortSoundModuleInstrument as EPSMInstrument
from .fds import FamilyDiskSystemInstrument as FDSInstrument
from .instrument import Instrument as Instrument
from .namco163 import Namco163Instrument as N163Instrument
from .vrc6 import VRC6Instrument as VRC6Instrument
from .vrc7 import VRC7Instrument as VRC7Instrument
from .wave_type import WaveType as WaveType

__all__ = [
    EPSMInstrument,
    FDSInstrument,
    Instrument,
    N163Instrument,
    VRC6Instrument,
    VRC7Instrument,
    WaveType,
]
