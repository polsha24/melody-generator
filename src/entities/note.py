"""
Сущность музыкальной ноты.
"""

from dataclasses import dataclass


@dataclass
class Note:
    """
    Представляет музыкальную ноту.

    Attributes:
        pitch: MIDI номер ноты (например, 60 = C4)
        duration: Длительность ноты в долях такта (например, 0.5 = восьмая)
    """

    pitch: int
    duration: float
