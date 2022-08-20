from typing import ClassVar, TypeVar
from weakref import WeakSet

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


def register(name: str) -> type[RegisterHandler]:
    return type(name, (RegisterHandler,), {"__slots__": (), "__registered_classes__": WeakSet()})
