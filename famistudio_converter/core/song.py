from collections.abc import Mapping

from attr import attrs


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class FamitrackerPattern:
    pattern_length: int
    beat_length: int
    tempo: int
    speed: int


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class FamistudioPattern:
    pattern_length: int
    beat_length: int
    note_length: int
    grove: list[int]
    grove_padding_mode: int


Pattern = FamitrackerPattern | FamistudioPattern
PatternList = list[FamitrackerPattern] | list[FamistudioPattern]


@attrs(slots=True, auto_attribs=True, eq=True, hash=True, frozen=True)
class Song:
    title: str
    length: int
    loop_point: int
    default_pattern: Pattern
    custom_pattern: Mapping[int, PatternList]
