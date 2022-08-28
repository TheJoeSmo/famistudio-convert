from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator, MutableMapping
from itertools import chain
from typing import final
from weakref import WeakKeyDictionary

from attr import attrs

from ...logging import log


class Meta(type):
    __handlers__: tuple[Handler, ...] = ()
    __wrapped_class_bases__: MutableMapping[type, tuple[type]] = WeakKeyDictionary()

    def __new__(meta, name, bases, attrs):
        cls = super().__new__(meta, name, bases, attrs)
        log.info(f"{meta.__name__} created class {cls.__name__}")
        cls.__wrapped_class_bases__[cls] = bases
        for handler in cls.get_handlers(cls):
            log.info(f"{cls.__name__} applying {handler.__name__}")  # type: ignore
            cls = handler.validate(cls)
        return cls

    @final
    @classmethod
    def get_handlers(cls, class_: type) -> Iterator[Handler]:
        class_handlers: tuple[Handler, ...] = *cls.__handlers__, *getattr(class_, "__handlers__", ())

        return chain(
            class_handlers,
            map(
                lambda b: cls.get_handlers(b),
                filter(lambda b: issubclass(b, Meta), cls.__wrapped_class_bases__[class_]),
            ),
        )


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Handler(ABC):
    @classmethod
    @abstractmethod
    def validate(cls, class_: type) -> type:
        ...
