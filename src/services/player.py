"""
Воспроизведение MIDI файлов через pygame.
"""

import time
from pathlib import Path
from typing import Union

import pygame
import pygame.midi


def init_player():
    """Инициализация pygame mixer для воспроизведения MIDI."""
    pygame.mixer.init()


def play_midi(
    midi_path: Union[str, Path],
    wait: bool = True,
) -> None:
    """
    Воспроизводит MIDI файл.

    Args:
        midi_path: Путь к MIDI файлу
        wait: Если True, блокирует выполнение до окончания воспроизведения
    """
    midi_path = Path(midi_path)
    if not midi_path.exists():
        raise FileNotFoundError(f"MIDI файл не найден: {midi_path}")

    if not pygame.mixer.get_init():
        init_player()

    pygame.mixer.music.load(str(midi_path))
    pygame.mixer.music.play()

    if wait:
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)


def stop_playback():
    """Останавливает текущее воспроизведение."""
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
