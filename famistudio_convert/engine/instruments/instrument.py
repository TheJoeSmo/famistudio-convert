from __future__ import annotations

from typing import ClassVar

from attr import attrs

from ...conversion import Attribute
from ...core import register
from ..envelope import Envelope
from ..expansion import Expansion

_InstrumentRegister = register("_InstrumentRegister", "__instrument_type__")


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Instrument(Attribute):
    __handlers__ = (_InstrumentRegister,)
    __instrument_type__: ClassVar[str | None] = None
    __expansion__: ClassVar[Expansion | None] = None

    title: str
    envelopes: list[Envelope]

    @classmethod
    def get_instrument_from_user(cls, instrument_name: str) -> type[Instrument]:
        return _InstrumentRegister.__registered_classes__[instrument_name]  # type: ignore
