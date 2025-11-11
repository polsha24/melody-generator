from dataclasses import dataclass
from typing import List
from .note import Note

@dataclass
class Melody:
    """
    Сгенерированная мелодия.

    notes -- последовательность нот
    tempo -- темп (ударов в минуту)
    bars -- количество тактов
    """
    notes: List[Note]
    tempo: int
    bars: int
