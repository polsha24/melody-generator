import time
from pathlib import Path
from typing import Union

import pygame
import pygame.midi


def init_player():
    """Initialize pygame mixer for MIDI playback."""
    pygame.mixer.init()


def play_midi(
    midi_path: Union[str, Path],
    wait: bool = True,
) -> None:
    """
    Play a MIDI file.

    Args:
        midi_path: Path to the MIDI file
        wait: If True, block until playback finishes
    """
    midi_path = Path(midi_path)
    if not midi_path.exists():
        raise FileNotFoundError(f"MIDI file not found: {midi_path}")

    # Initialize if not already
    if not pygame.mixer.get_init():
        init_player()

    # Load and play
    pygame.mixer.music.load(str(midi_path))
    pygame.mixer.music.play()

    if wait:
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)


def stop_playback():
    """Stop any currently playing music."""
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
