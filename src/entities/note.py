from dataclasses import dataclass

@dataclass
class Note:
    """
    Представляет музыкальную ноту.

    name -- название ноты (например, "C", "D")
    midi -- MIDI номер ноты (например, 60)
    duration -- длительность ноты в долях такта (например, 1.0 = четверть, 0.5 = восьмая)
    """
    name: str
    midi: int
    duration: float 
