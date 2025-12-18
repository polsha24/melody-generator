from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ScaleType(Enum):
    """Типы музыкальных гамм"""

    MAJOR = "major"
    MINOR = "minor"
    PENTATONIC_MAJOR = "pentatonic_major"
    PENTATONIC_MINOR = "pentatonic_minor"
    BLUES = "blues"
    DORIAN = "dorian"
    MIXOLYDIAN = "mixolydian"


# Интервальные формулы для каждого типа гаммы
SCALE_INTERVALS: Dict[ScaleType, List[int]] = {
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    ScaleType.MINOR: [0, 2, 3, 5, 7, 8, 10],
    ScaleType.PENTATONIC_MAJOR: [0, 2, 4, 7, 9],
    ScaleType.PENTATONIC_MINOR: [0, 3, 5, 7, 10],
    ScaleType.BLUES: [0, 3, 5, 6, 7, 10],
    ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],
    ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
}

# Названия нот -> MIDI номер (октава 4)
NOTE_TO_MIDI: Dict[str, int] = {
    "C": 60,
    "C#": 61,
    "Db": 61,
    "D": 62,
    "D#": 63,
    "Eb": 63,
    "E": 64,
    "F": 65,
    "F#": 66,
    "Gb": 66,
    "G": 67,
    "G#": 68,
    "Ab": 68,
    "A": 69,
    "A#": 70,
    "Bb": 70,
    "B": 71,
}


@dataclass
class Scale:
    """
    Музыкальная гамма, содержит доступные высоты нот.

    root -- корневая нота гаммы как MIDI номер (например, 60 == C4)
    intervals -- интервальная формула, например [0, 2, 4, 5, 7, 9, 11]
    """

    root: int
    intervals: List[int]

    @classmethod
    def from_key(cls, key: str, scale_type: ScaleType = ScaleType.MAJOR) -> "Scale":
        """
        Создаёт гамму из названия ноты и типа гаммы.

        Args:
            key: Название ноты (например, "C", "F#", "Bb")
            scale_type: Тип гаммы

        Returns:
            Scale объект
        """
        key_upper = key.capitalize()
        if key_upper not in NOTE_TO_MIDI:
            available = ", ".join(sorted(set(NOTE_TO_MIDI.keys())))
            raise ValueError(f"Unknown key: {key}. Available: {available}")

        root = NOTE_TO_MIDI[key_upper]
        intervals = SCALE_INTERVALS[scale_type]
        return cls(root=root, intervals=intervals)
