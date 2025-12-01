from dataclasses import dataclass


@dataclass
class Note:
    """
    Представляет музыкальную ноту.

    pitch -- MIDI номер ноты (например, 60)
    duration -- длительность ноты в долях такта (например, 0.5 = восьмая)
    """

    pitch: int
    duration: float
