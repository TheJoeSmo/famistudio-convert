from collections.abc import Callable
from typing import Any, TypeVar, overload

_T = TypeVar("_T")
_P = TypeVar("_P")


def is_type(type_: type[_P]) -> Callable[[Any, Callable[[_P], _T]], _T | None]:
    def condition_is_type(value: _P, result: Callable[[_P], _T]) -> _T | None:
        return result(value) if isinstance(value, type_) else None

    return condition_is_type


def is_not_type(type_: type[Any]) -> Callable[[Any, Callable[[Any], _T]], _T | None]:
    def condition_is_not_type(value: _P, result: Callable[[_P], _T]) -> _T | None:
        return None if isinstance(value, type_) else result(value)

    return condition_is_not_type


@overload
def is_not_none(value: None, result: Any) -> None:
    ...


@overload
def is_not_none(value: _P, result: Callable[[_P], _T | None] | _T) -> _T:
    ...


def is_not_none(value: _P, result: Callable[[_P], _T | None] | _T) -> _T | None:
    return None if value is None else result(value) if isinstance(result, Callable) else result


def is_none(value: Any, result: Callable[[], _T | None] | _T) -> _T | None:
    return None if value is not None else result() if isinstance(result, Callable) else result
