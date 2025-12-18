"""
Настройки генератора мелодий.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class GeneratorSettings:
    """
    Настройки для генерации мелодии.

    Attributes:
        length: Количество нот в мелодии
        allowed_durations: Допустимые длительности нот (в долях такта)
        octave_range: Диапазон октав (+/- от корневой ноты)
    """

    length: int
    allowed_durations: List[float]
    octave_range: int
