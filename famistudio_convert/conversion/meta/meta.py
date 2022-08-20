from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator, MutableMapping
from itertools import chain
from typing import final
from weakref import WeakKeyDictionary

from attr import attrs


class Meta(type):
    __handlers__: tuple[Handler, ...] = ()
    __wrapped_class_bases__: MutableMapping[type, tuple[type]] = WeakKeyDictionary()

    def __new__(meta, name, bases, attrs):
        cls = type.__new__(meta, name, bases, attrs)
        meta.__wrapped_class_bases__[cls] = bases
        for handler in cls.get_handlers(cls):
            cls = handler.validate(cls)
        return cls

    @final
    @classmethod
    def get_handlers(cls, class_: type) -> Iterator[Handler]:
        return chain(
            cls.__handlers__,
            map(
                lambda b: cls.get_handlers(b),
                filter(lambda b: issubclass(b, Meta), cls.__wrapped_class_bases__[class_]),
            ),
        )  # type: ignore


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Handler(ABC):
    @classmethod
    @abstractmethod
    def validate(cls, class_: type) -> type:
        ...
