from logging import WARN
from typing import ClassVar, TypeVar, overload
from weakref import WeakSet, WeakValueDictionary

from attr import attrs

from ...logging import log
from .meta import Handler

_T = TypeVar("_T", bound=type)


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class RegisterHandler(Handler):
    __registered_classes__: ClassVar[WeakSet[type]] = WeakSet()

    @classmethod
    def validate(cls, class_: _T) -> _T:
        log.info(f"{cls} registered {class_.__class__.__name__}")
        cls.__registered_classes__.add(class_)
        return class_


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class RegisterMapHandler(Handler):
    __registered_classes__: ClassVar[WeakValueDictionary[str, type]] = WeakValueDictionary()
    __attribute__: ClassVar[str] = "__attribute__"

    @classmethod
    def validate(cls, class_: _T) -> _T:
        name = getattr(class_, cls.__attribute__)
        if name is None:
            name = class_.__name__
        log.info(f"{cls.__name__} registered {class_.__name__}")
        if (
            log.isEnabledFor(WARN)
            and name in cls.__registered_classes__
            and repr(cls.__registered_classes__[name]) != repr(class_)
        ):
            log.warning(
                f"{cls.__name__} has naming conflict between {class_} and "
                + f"{cls.__registered_classes__[name]} with name {name}"
            )
        cls.__registered_classes__[name] = class_
        return class_


@overload
def register(name: str, attribute: None = None) -> type[RegisterHandler]:
    ...


@overload
def register(name: str, attribute: str) -> type[RegisterMapHandler]:
    ...


def register(name: str, attribute: str | None = None) -> type[RegisterHandler | RegisterMapHandler]:
    if attribute is None:
        result = type(name, (RegisterHandler,), {"__slots__": (), "__registered_classes__": WeakSet()})
    else:
        result = type(
            name,
            (RegisterMapHandler,),
            {"__slots__": (), "__registered_classes__": WeakValueDictionary(), "__attribute__": attribute},
        )
    log.info(f"Created {name}")
    return result
