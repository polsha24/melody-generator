"""
Сущность мелодии — последовательность нот.
"""

from dataclasses import dataclass
from typing import List

from .note import Note


@dataclass
class Melody:
    """
    Сгенерированная мелодия.

    Attributes:
        notes: Последовательность нот
    """

    notes: List[Note]

    def total_duration(self) -> float:
        """
        Вычисляет сумму длительностей всех нот в долях.
        """
        return sum(n.duration for n in self.notes)
