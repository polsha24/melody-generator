from dataclasses import dataclass
from typing import List

@dataclass
class Scale:
    """
    Музыкальная гамма, содержит доступные высоты нот.

    name -- название гаммы, например "C major"
    notes -- MIDI высоты доступных нот в этой гамме
    """
    name: str
    notes: List[int]
