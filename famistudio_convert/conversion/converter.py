from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import suppress
from logging import warn
from typing import ClassVar, TypeVar

from attr import attrs

from ..core import Meta, register
from .pattern import GreedyHandler, Handler, InvalidPatternException, Pattern
from .types import ConversionType, load_internal

_T = TypeVar("_T")
_A = TypeVar("_A", bound="Attribute")


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class WordHandler(Handler):
    @classmethod
    def solve(cls, _, found: str) -> str:
        return found


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class FieldDataHandler(Handler):
    @classmethod
    def validate_balanced_brackets(cls, string: str) -> tuple[int, int]:
        # sourcery skip: for-index-underscore, remove-unused-enumerate
        brackets = deque()
        d = {}
        for i, c in enumerate(string):
            match c:
                case "(":
                    brackets.append(i)
                case ")":
                    try:
                        d[brackets.pop()] = i
                    except IndexError as e:
                        raise InvalidPatternException(f"'{string}' contains too many closing parentheses") from e

        if brackets:
            raise InvalidPatternException(f"'{string}' contains too many opening parentheses")

        first_bracket = min(d.keys())
        return first_bracket, d[first_bracket]

    @classmethod
    def solve(cls, _, found: str) -> str:
        start, end = cls.validate_balanced_brackets(found)
        return found[start + 1 : end - 1]


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class HandleNewLine(Handler):
    @classmethod
    def solve(cls, *_) -> str:
        return "\n"


WORD_PATTERN = Pattern("(\\w)", WordHandler())
FIELD_DATA_PATTERN = Pattern("((.|\\n)*)", WordHandler())
NEW_LINE_PATTERN = Pattern("new_line", HandleNewLine())


_RegisterAttribute = register("_RegisterAttribute", "__title__")


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Attribute:
    __metaclass__ = Meta
    __handlers__ = (_RegisterAttribute,)
    __title__: ClassVar[str | None] = None
    __load_data__: ClassVar[list[Callable[[ConversionType], str]]] = [load_internal]
    __field_types__: ClassVar[dict[ConversionType, Mapping[type[Attribute], str]]] = {}

    @staticmethod
    def register_loading_method(function: Callable[[ConversionType], str]) -> None:
        Attribute.__load_data__.append(function)

    @classmethod
    @property
    def title(cls) -> str:
        return cls.__name__ if cls.__title__ is None else cls.__title__

    @classmethod
    def get_data(cls, type: ConversionType) -> str:
        for function in cls.__load_data__:
            with suppress(NotImplementedError):
                return function(type)
        raise NotImplementedError

    @classmethod
    def parse_fields(cls, data: str) -> Mapping[str, str]:
        fields = data.split("$$")
        parsed_fields = {}
        for field in fields:
            field_name = WORD_PATTERN.solve(cls, field)
            field_data = FIELD_DATA_PATTERN.solve(cls, field[field_name:])
            if field_name in parsed_fields:
                warn(f"{field_name} is already defined")
            parsed_fields |= {field_name: field_data}
        return parsed_fields

    @classmethod
    def validate_field_name(cls, field: str) -> type[Attribute]:
        try:
            return _RegisterAttribute.__registered_classes__[field]  # type: ignore
        except KeyError as e:
            raise InvalidPatternException(f"{field} is not a valid attribute") from e

    @classmethod
    def validate_field_names(cls, fields: Iterable[str]) -> Sequence[tuple[str, type[Attribute]]]:
        return [(field, cls.validate_field_name(field)) for field in fields]

    @classmethod
    def validate_fields(cls, fields: Mapping[str, str]) -> Mapping[type[Attribute], str]:
        return {f_type: fields[f_key] for (f_key, f_type) in cls.validate_field_names(fields.keys())}

    @classmethod
    def file_from_type(cls, type: ConversionType) -> str:
        if type not in cls.__field_types__:
            cls.__field_types__[type] = cls.validate_fields(cls.parse_fields(cls.get_data(type)))
        return cls.__field_types__[type][cls]

    def solve(self, type: ConversionType, layer: int) -> str:
        return solve(self, self.file_from_type(type), type, layer)

    @classmethod
    def _solve_attribute(cls, attribute: object, type_: ConversionType, stared: bool, layer: int) -> str:
        attribute_type = type(attribute)
        match attribute_type:
            case int() | str() | float() | bool() as attribute_type:
                return str(attribute)
            case list() | tuple() | set() as attribute_type:
                objs = [cls._solve_attribute(obj, type_, False, layer + 1) for obj in attribute]  # type: ignore
                return ", ".join(objs) if stared else "\t" * layer + "\n".join(objs)
            case Attribute() as attribute_type:
                return attribute.solve(attribute, type, layer + 1)  # type: ignore
            case _:
                raise NotImplementedError

    def solve_attribute(self, attribute_name: str, type: ConversionType, stared: bool = False, layer: int = 0) -> str:
        return self._solve_attribute(getattr(self, attribute_name), type, stared, layer)


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class InternalHandler(GreedyHandler[_T]):
    __handlers__ = (NEW_LINE_PATTERN,)


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class StaredAttributeHandler(Handler[_A]):
    @classmethod
    def solve(cls, obj: _A, found: str, type: ConversionType = ConversionType.default, layer: int = 0) -> str:
        return obj.solve_attribute(found, type, True, layer)


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class SimpleAttributeHandler(Handler[_A]):
    @classmethod
    def solve(cls, obj: _A, found: str, type: ConversionType = ConversionType.default, layer: int = 0) -> str:
        return obj.solve_attribute(found, type, False, layer)


INTERNAL_PATTERN = Pattern("\\$#([a-zA-Z0-9_]+)", InternalHandler())
STARED_PATTERN = Pattern("\\$\\*([a-zA-Z0-9_]+)", StaredAttributeHandler())
SIMPLE_PATTERN = Pattern("\\*([a-zA-Z0-9_]+)", SimpleAttributeHandler())


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class AttributeHandler(GreedyHandler[_T]):
    __handlers__ = (INTERNAL_PATTERN, STARED_PATTERN, SIMPLE_PATTERN)


ATTRIBUTE_PATTERN = Pattern("\\$([\\s\\S]*)", AttributeHandler())


def solve(cls: object, string: str, type: ConversionType, layer: int) -> str:
    return ATTRIBUTE_PATTERN.solve(cls, string, type=type, layer=layer)
