from __future__ import annotations

from enum import Enum, auto

from pkg_resources import resource_filename

FAMISTUDIO_TEXT_PATH = "../data/famistudio_text.txt"


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
            path = resource_filename(__package__, FAMISTUDIO_TEXT_PATH)
        case _:
            raise NotImplementedError
    with open(resource_filename(__package__, path)) as f:
        return f.read()
