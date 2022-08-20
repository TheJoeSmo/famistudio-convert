from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from attr import attrs

from ..envelope import Envelope
from ..expansion import Expansion

_models = {}


class MetaInstrument(type):
    def __new__(meta, name, bases, attrs):
        cls: type[Instrument] = type.__new__(meta, name, bases, attrs)  # type: ignore
        for name in cls.__user_names__:
            meta.register(name, cls)
        return cls

    @classmethod
    def register(cls, name: str, type):
        _models[name] = type


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Instrument:
    __meta_class__: ClassVar[type] = MetaInstrument
    __user_names__: ClassVar[Sequence[str]] = ()
    __expansion__: ClassVar[Expansion | None] = None

    title: str
    envelope: list[Envelope]

    @classmethod
    def get_instrument_from_user(cls, instrument_name: str) -> type[Instrument]:
        return _models[instrument_name]
