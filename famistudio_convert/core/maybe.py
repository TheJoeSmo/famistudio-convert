from collections.abc import Callable, Iterator
from typing import TypeVar, overload

_T = TypeVar("_T")


@overload
def maybe(
    *items: Callable[[], _T | None] | Iterator[Callable[[], _T | None]], start: _T | None = None, exception: None = None
) -> _T | None:
    ...


@overload
def maybe(
    *items: Callable[[], _T | None] | Iterator[Callable[[], _T | None]], start: _T | None = None, exception: Callable
) -> _T:
    ...


def maybe(
    *items: Callable[[], _T | None] | Iterator[Callable[[], _T | None]],
    start: _T | None = None,
    exception: Callable | None = None
) -> _T | None:
    if start is not None:
        return start
    for item in items:
        functions = item if isinstance(item, Iterator) else (item,)
        for function in functions:
            start = function()
            if start is not None:
                return start
    if exception is not None:
        exception()
    return None
