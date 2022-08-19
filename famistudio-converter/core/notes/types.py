from enum import Enum, auto


class NoteType:
    pass


class MusicalNoteType(int, NoteType, Enum):
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    F_SHARP = 5
    F = 6
    G_SHARP = 7
    G = 8
    A_SHARP = 9
    A = 10
    B_SHARP = 11


class SpecialNoteType(int, NoteType, Enum):
    STOP = auto()
    RELEASE = auto()
