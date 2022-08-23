from typing import ClassVar, TypeVar, overload
from weakref import WeakSet, WeakValueDictionary

from attr import attrs

from .meta import Handler

_T = TypeVar("_T", bound=type)


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class RegisterHandler(Handler):
    __registered_classes__: ClassVar[WeakSet[type]] = WeakSet()

    @classmethod
    def validate(cls, class_: _T) -> _T:
        cls.__registered_classes__.add(class_)
        return class_


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class RegisterMapHandler(Handler):
    __registered_classes__: ClassVar[WeakValueDictionary[str, type]] = WeakValueDictionary()
    __attribute__: ClassVar[str] = "__attribute__"

    @classmethod
    def validate(cls, class_: _T) -> _T:
        cls.__registered_classes__[getattr(class_, cls.__attribute__)] = class_
        return class_


@overload
def register(name: str, attribute: None = None) -> type[RegisterHandler]:
    ...


@overload
def register(name: str, attribute: str) -> type[RegisterMapHandler]:
    ...


def register(name: str, attribute: str | None = None) -> type[RegisterHandler | RegisterMapHandler]:
    if attribute is None:
        return type(name, (RegisterHandler,), {"__slots__": (), "__registered_classes__": WeakSet()})
    return type(
        name,
        (RegisterMapHandler,),
        {"__slots__": (), "__registered_classes__": WeakValueDictionary(), "__attribute__": attribute},
    )
