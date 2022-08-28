from __future__ import annotations

from enum import Enum, auto

from ..data import read_text

FAMISTUDIO_TEXT_PATH = "famistudio_text.txt"


class ConversionType:
    @classmethod
    @property
    def default(cls) -> ConversionType:
        return InternalConversionType.FAMISTUDIO_TEXT


class InternalConversionType(ConversionType, Enum):
    FAMISTUDIO_TEXT = auto()


def load_internal(conversion_type: ConversionType) -> str:
    match conversion_type:
        case InternalConversionType.FAMISTUDIO_TEXT:
            path = FAMISTUDIO_TEXT_PATH
        case _:
            raise NotImplementedError
    return read_text(path)
