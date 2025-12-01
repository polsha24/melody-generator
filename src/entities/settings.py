from dataclasses import dataclass


@dataclass
class GeneratorSettings:
    length: int  # количество нот
    allowed_durations: list[float]  # допустимые длительности нот
    octave_range: int  # +/- сколько октав можно прыгать от root
