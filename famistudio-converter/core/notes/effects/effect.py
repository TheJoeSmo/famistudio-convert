from collections.abc import Sequence
from typing import ClassVar

from attr import attrs

_effects = {}


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class MetaEffect(type):
    def __new__(meta, name, bases, attrs):
        cls: type[Effect] = type.__new__(meta, name, bases, attrs)  # type: ignore
        for name in cls.__user_names__:
            meta.register(name, cls)
        return cls

    @classmethod
    def register(cls, name: str, type):
        _effects[name] = type


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Effect:
    __meta_class__: ClassVar[type] = MetaEffect
    __user_names__: ClassVar[Sequence[str]] = ()
