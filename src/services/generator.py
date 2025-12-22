"""
Генератор случайных мелодий.
"""

import random

from ..entities.melody import Melody  # from src.entities import Melody, Note, Scale, GeneratorSettings
from ..entities.note import Note
from ..entities.scale import Scale
from ..entities.settings import GeneratorSettings


class MelodyGenerator:
    """Класс для генерации мелодий на основе гаммы и настроек."""

    def __init__(self, scale: Scale, settings: GeneratorSettings):
        """
        Инициализация генератора.

        Args:
            scale: Музыкальная гамма
            settings: Настройки генерации
        """
        self.scale = scale
        self.settings = settings

    def generate(self) -> Melody:
        """
        Генерирует новую мелодию.
        """
        notes = []

        for _ in range(self.settings.length):
            pitch = self._random_pitch()
            duration = random.choice(self.settings.allowed_durations)
            notes.append(Note(pitch=pitch, duration=duration))

        return Melody(notes)

    def _random_pitch(self) -> int:
        """
        Возвращает MIDI номер случайной ноты в рамках гаммы.
        """
        interval = random.choice(self.scale.intervals)
        octave_shift = random.randint(
            -self.settings.octave_range, self.settings.octave_range
        )
        return self.scale.root + interval + 12 * octave_shift
