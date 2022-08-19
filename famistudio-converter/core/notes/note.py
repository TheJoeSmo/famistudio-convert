from abc import ABC, abstractmethod

from ..arpeggio import Arpeggio
from ..instruments import Instrument
from .types import NoteType


class Note(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def type(self) -> NoteType:
        ...

    @property
    @abstractmethod
    def value(self) -> int:
        ...

    @property
    @abstractmethod
    def duration(self) -> int:
        ...

    @property
    def release(self) -> int | None:
        return None

    @property
    def instrument(self) -> Instrument | None:
        return None

    @property
    def arpeggio(self) -> Arpeggio | None:
        return None
