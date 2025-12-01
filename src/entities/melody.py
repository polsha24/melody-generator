from dataclasses import dataclass
from typing import List

from .note import Note


@dataclass
class Melody:
    """
    Сгенерированная мелодия.

    notes -- последовательность нот
    """

    notes: List[Note]

    def total_duration(self) -> float:
        return sum(n.duration for n in self.notes)
