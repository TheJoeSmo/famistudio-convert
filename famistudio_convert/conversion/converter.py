from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import suppress
from enum import Enum
from logging import INFO, WARN
from typing import ClassVar, TypeVar

from attr import attrs
from regex import Match, search

from famistudio_convert.core.meta.register import RegisterMapHandler

from ..core import Meta, register
from ..logging import log
from .pattern import GreedyHandler, Handler, InvalidPatternException, Pattern
from .types import ConversionType, load_internal

_T = TypeVar("_T")
_A = TypeVar("_A", bound="Attribute")
_new_line_char = "\n"


@attrs(slots=True, auto_attribs=True, eq=True)
class WordHandler(Handler):
    @classmethod
    def solve(cls, _, found: str) -> str:
        log.info(f"{cls.__name__} found '{found}'")
        return found


@attrs(slots=True, auto_attribs=True, eq=True)
class FieldDataHandler(Handler):
    @classmethod
    def validate_balanced_brackets(cls, string: str) -> None:
        # sourcery skip: for-index-underscore, remove-unused-enumerate
        brackets: deque[int] = deque()
        d: dict[int, int] = {}
        for i, c in enumerate(string):
            match c:
                case "[":
                    brackets.append(i)
                case "]":
                    try:
                        d[brackets.pop()] = i
                    except IndexError as e:
                        log.error(f"{cls.__name__} found too many closing brackets for {string.split(_new_line_char)}")
                        raise InvalidPatternException(f"'{string}' contains too many closing brackets") from e

        if brackets:
            log.error(f"{cls.__name__} found too many opening brackets for {string.split(_new_line_char)}")
            raise InvalidPatternException(f"'{string}' contains too many opening brackets")

    @classmethod
    def solve(cls, _, found: str) -> str:
        cls.validate_balanced_brackets(found)
        return found


@attrs(slots=True, auto_attribs=True, eq=True)
class HandleNewLine(Handler):
    @classmethod
    def solve(cls, *_) -> str:
        log.debug(f"{cls.__name__} added a new line")
        return "\n"


WORD_PATTERN: Pattern = Pattern("([\\w]+)", WordHandler())
FIELD_DATA_PATTERN: Pattern = Pattern("\\[([^\\]\\[]*+(?:(?R)[^\\[\\]]*)*+)\\]", FieldDataHandler())
OPTIONAL_FIELD_DATA: str = "([_a-zA-Z][_a-zA-Z0-9]*)\\[([^\\]\\[]*+(?:(?R)[^\\[\\]]*)*+)\\]"
NEW_LINE_PATTERN: Pattern = Pattern("new_line", HandleNewLine())


_RegisterAttribute: type[RegisterMapHandler] = register("_RegisterAttribute", "__title__")


class Attribute(metaclass=Meta):
    __handlers__ = (_RegisterAttribute,)
    __title__: ClassVar[str | None] = None
    __load_data__: ClassVar[list[Callable[[ConversionType], str]]] = [load_internal]
    __field_types__: ClassVar[dict[ConversionType, Mapping[type[Attribute], str]]] = {}
    __slots__ = ()

    @staticmethod
    def register_loading_method(function: Callable[[ConversionType], str]) -> None:
        if log.isEnabledFor(INFO):
            log.info(f"{Attribute.__name__} registered {function}")
        Attribute.__load_data__.append(function)

    @classmethod
    @property
    def title(cls) -> str:
        return cls.__name__ if cls.__title__ is None else cls.__title__

    @classmethod
    def get_data(cls, type: ConversionType) -> str:
        log.info(f"{cls.__name__} is loading data for '{type}'")
        for function in cls.__load_data__:
            with suppress(NotImplementedError):
                result = function(type)
                log.info(f"{cls.__name__} found {result.split(_new_line_char)} for '{type}'")
                return result
        log.error(f"{cls.__name__} did not find any data for '{type}'")
        raise NotImplementedError

    @classmethod
    def parse_fields(cls, data: str) -> Mapping[str, str]:
        fields: list[str] = data.split("$$")[1:]
        log.info(f"{cls.__name__} parsing {len(fields)} fields from {data.split(_new_line_char)}")
        parsed_fields: dict[str, str] = {}
        for field in fields:
            log.info(f"{cls.__name__} parsing {field.split(_new_line_char)}")
            field_name = WORD_PATTERN.solve_next_match(cls, field)
            if log.isEnabledFor(WARN) and field_name in parsed_fields:
                log.warning(f"{field_name} is already defined")
            field_data = FIELD_DATA_PATTERN.solve_next_match(cls, field[len(field_name) :])
            log.info(f"{cls.__name__} found {field_name} with data {field_data.split(_new_line_char)}")
            parsed_fields |= {field_name: field_data}
        return parsed_fields

    @classmethod
    def validate_field_name(cls, field: str) -> type[Attribute]:
        try:
            result = _RegisterAttribute.__registered_classes__[field]
        except KeyError as e:
            log.error(
                f"{cls.__name__} does not have a valid attribute of name '{field}' "
                + f"inside {[c.__name__ for c in _RegisterAttribute.__registered_classes__.values()]}"
            )
            raise InvalidPatternException(f"{field} is not a valid attribute") from e
        log.info(f"{cls.__name__} found {result.__name__} for field '{field}'")
        return result  # type: ignore

    @classmethod
    def validate_field_names(cls, fields: Iterable[str]) -> Sequence[tuple[str, type[Attribute]]]:
        log.info(f"{cls.__name__} validating field names from {fields}")
        results = [(field, cls.validate_field_name(field)) for field in fields]
        log.info(f"{cls.__name__} validated field names {[(n, a.__name__) for (n, a) in results]}")
        return results

    @classmethod
    def validate_fields(cls, fields: Mapping[str, str]) -> Mapping[type[Attribute], str]:
        return {f_type: fields[f_key] for (f_key, f_type) in cls.validate_field_names(fields.keys())}

    @classmethod
    def file_from_type(cls, type: ConversionType) -> str:
        if type not in cls.__field_types__:
            log.info(f"{cls.__name__} loading file from '{type}'")
            cls.__field_types__[type] = cls.validate_fields(cls.parse_fields(cls.get_data(type)))
        return cls.__field_types__[type][cls]

    def solve(self, type: ConversionType, layer: int) -> str:
        return _solve(self, self.file_from_type(type), type, layer)

    @classmethod
    def _solve_attribute(cls, attribute: object, type_: ConversionType, stared: bool, layer: int) -> str:
        if isinstance(attribute, (int, str, float, bool, Enum)):
            return str(attribute)
        elif isinstance(attribute, (list, tuple, set)):
            objs = [cls._solve_attribute(obj, type_, False, layer + 1) for obj in attribute]  # type: ignore
            return ", ".join(objs) if stared else "\t" * layer + "\n".join(objs)
        elif isinstance(attribute, Attribute):
            return attribute.solve(attribute, type, layer + 1)  # type: ignore

        log.error(f"{cls.__name__} does not implement a way to solve for {attribute.__class__.__name__}")
        raise NotImplementedError

    def solve_attribute(self, attribute_name: str, type: ConversionType, stared: bool = False, layer: int = 0) -> str:
        attribute = getattr(self, attribute_name)
        log.info(
            f"{self.__class__.__name__} solving for attribute '{attribute_name}' {attribute} for '{type}' "
            + f"on layer {layer} {'as a stared attribute' if stared else ''}"
        )
        result = self._solve_attribute(attribute, type, stared, layer)
        log.info(f"{self.__class__.__name__} provided '{result!s}' for {attribute_name} of type '{type}'")
        return result


class AttributePattern(Attribute, Pattern):
    __slots__ = ()


@attrs(slots=True, auto_attribs=True, eq=True)
class InternalHandler(GreedyHandler[_T]):
    __patterns__ = (NEW_LINE_PATTERN,)


@attrs(slots=True, auto_attribs=True, eq=True)
class OptionalHandler(Handler[_A]):
    @classmethod
    def solve(cls, obj: _A, found: str, *args, **kwargs) -> str:
        log.info(f"{cls.__name__} is solving '{found}' with {args} and {kwargs}")
        re_match: Match[str] | None = search(OPTIONAL_FIELD_DATA, found[1:])
        if re_match is None:
            log.error(f"{cls.__name__} could not resolve optional field '{found[1:]}' with '{OPTIONAL_FIELD_DATA}'")
            raise ValueError(f"{cls.__name__} could not resolve optional field '{found[1:]}'")
        attribute_name: str = re_match[1]
        result: str = ATTRIBUTE_PATTERN.solve(obj, re_match[2]) if getattr(obj, attribute_name, None) else ""
        log.info(f"{cls.__name__} provided '{result}' from '{found}' with {args} and {kwargs}")
        return result


@attrs(slots=True, auto_attribs=True, eq=True)
class StaredAttributeHandler(Handler[_A]):
    @classmethod
    def solve(cls, obj: _A, found: str, type: ConversionType = ConversionType.default, layer: int = 0) -> str:
        log.info(f"{cls.__name__} is solving '{found}' for {obj.__class__.__name__} of '{type}' on layer {layer}")
        return obj.solve_attribute(found[2:], type, True, layer)


@attrs(slots=True, auto_attribs=True, eq=True)
class SimpleAttributeHandler(Handler[_A]):
    @classmethod
    def solve(cls, obj: _A, found: str, type: ConversionType = ConversionType.default, layer: int = 0) -> str:
        log.info(f"{cls.__name__} is solving '{found}' for {obj.__class__.__name__} of '{type}' on layer {layer}")
        return obj.solve_attribute(found[1:], type, False, layer)


INTERNAL_PATTERN: Pattern = Pattern("(\\$#[a-zA-Z0-9_]+)", InternalHandler())
OPTIONAL_PATTERN: Pattern = Pattern(
    "(\\$[_a-zA-Z][_a-zA-Z0-9]*\\[([^\\]\\[]*+(?:(?R)[^\\[\\]]*)*+)\\])", OptionalHandler()
)
STARED_PATTERN: Pattern = Pattern("(\\$\\*[_a-zA-Z][_a-zA-Z0-9]*)", StaredAttributeHandler())
SIMPLE_PATTERN: Pattern = Pattern("(\\$[_a-zA-Z][_a-zA-Z0-9]*)", SimpleAttributeHandler())


@attrs(slots=True, auto_attribs=True, eq=True)
class AttributeHandler(GreedyHandler[_T]):
    __patterns__ = (OPTIONAL_PATTERN, INTERNAL_PATTERN, STARED_PATTERN, SIMPLE_PATTERN)


ATTRIBUTE_PATTERN: Pattern = Pattern(
    "(\\$[_a-zA-Z][_a-zA-Z0-9]+(\\[([^\\]\\[]*+(?:(?R)[^\\[\\]]*)*+)\\])?)", AttributeHandler()
)


def _solve(cls: Attribute, string: str, type: ConversionType, layer: int) -> str:
    return ATTRIBUTE_PATTERN.solve(cls, string, type=type, layer=layer)


def solve(cls: Attribute, string: str, type: ConversionType) -> str:
    return _solve(cls, string, type, 0)
