from __future__ import annotations

from collections.abc import Sequence
from logging import warn
from typing import Any, ClassVar, Generic, TypeVar, get_type_hints

from attr import attrs

from .meta.meta import Handler

_T = TypeVar("_T")
_P = TypeVar("_P", bound="Converter")
_converters: list[type[Converter]] = []


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class FieldGenerator:
    attribute_name: str
    title: str | None = None
    new_line: bool = False
    add_indent: bool = False


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class _FieldGenerator(Generic[_T, _P]):
    title: str
    attribute_name: str
    new_line: bool
    add_indent: bool
    field_type: type[_T]
    underlying_class: type[_P]

    def to_field(self, class_: _P) -> Field[_T]:
        if not isinstance(class_, self.underlying_class):
            warn(f"{class_} is not {self.underlying_class.__name__}")
        attribute = getattr(self.underlying_class, self.attribute_name)
        if not isinstance(attribute, self.field_type):
            warn(
                f"{self.underlying_class.__name__}::{self.attribute_name} is not a "
                + f"{self.field_type.__name__} but {attribute}"
            )
        return Field(self.title, self.new_line, self.add_indent, attribute)


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Field(Generic[_T]):
    title: str
    new_line: bool
    add_indent: bool
    value: _T

    def to_text(self, indentation: int) -> tuple[int, str]:
        updated_indentation = indentation + int(self.add_indent)
        if self.new_line:
            return updated_indentation, "\t" * indentation + ""
        else:
            return updated_indentation, "\t" * indentation + f'{self.title}="{self.value}'


class MetaConverter(Handler):
    @classmethod
    def validate(cls, class_: type[Converter]) -> type[Converter]:
        cls.fix_valid_titles(class_)
        cls.register(class_)
        class_.__validated_fields__ = tuple(cls.validate_fields(class_, class_.__fields__))
        return class_

    @classmethod
    def validate_fields(cls, class_: type[Converter], fields: Any) -> Sequence[_FieldGenerator]:
        if not isinstance(fields, Sequence):
            raise TypeError(f"Fields must be a tuple of fields, not {fields}")
        validated_fields = []
        for index, field in enumerate(fields):
            if not isinstance(field, FieldGenerator):
                raise TypeError(f"{class_}::__fields__[{index}] must be a {FieldGenerator.__name__} not {field}")
            validated_fields.append(cls.generate_field_from_attribute(class_, field))
        return validated_fields

    @classmethod
    def generate_field_from_attribute(cls, class_: type[Converter], field: FieldGenerator) -> _FieldGenerator:
        attribute = get_type_hints(class_).get(field.attribute_name, None)
        if attribute is None:
            raise KeyError(f"{field.attribute_name} must have type hints provided inside {class_.__name__}")
        if field.title is None and not issubclass(attribute, Converter):
            raise TypeError(f"{class_.__name__}::{field.attribute_name} must define a title for a field")
        title = attribute.title_suggestion if field.title is None else field.title
        return _FieldGenerator(title, field.attribute_name, field.new_line, field.add_indent, attribute, class_)

    @classmethod
    def register(cls, type):
        _converters.append(type)

    @classmethod
    def fix_valid_titles(cls, class_):
        titles = getattr(class_, "__valid_titles__", None)
        if titles is None:
            raise TypeError(f"{class_.__name__} must define '__valid_titles__'")
        if isinstance(titles, str):
            titles = (titles,)
        if not isinstance(titles, Sequence):
            raise TypeError(f"{class_.__name__}::'__valid_titles__' must be a Sequence")
        if len(titles) <= 0:
            raise ValueError(f"{class_.__name__}::'__valid_titles__' must contain one or more titles")
        class_.__valid_titles__ = titles


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Converter:
    __meta_class__: ClassVar[type] = MetaConverter
    __fields__: ClassVar[tuple[FieldGenerator, ...]] = ()
    __valid_titles__: ClassVar[str | tuple[str, ...]] = ()
    __validated_fields__: ClassVar[tuple[_FieldGenerator]]

    @classmethod
    @property
    def valid_titles(cls) -> tuple[str]:
        return cls.__valid_titles__  # type: ignore

    @classmethod
    @property
    def title_suggestion(cls) -> str:
        return cls.valid_titles[0]

    @property
    def fields(self) -> Sequence[Field]:
        return tuple(field.to_field(self) for field in self.__validated_fields__)
