from dataclasses import dataclass
from typing import List


@dataclass
class Scale:
    """
    Музыкальная гамма, содержит доступные высоты нот.

    root -- корневая нота гаммы как MIDI номер (например, 60 == C4)
    intervals -- интервальная формула, например [0, 2, 4, 5, 7, 9, 11]
    """

    root: int
    intervals: List[int]
