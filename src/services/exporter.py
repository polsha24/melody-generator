"""
Экспорт мелодий в формат MIDI.
"""

from pathlib import Path
from typing import Union

import mido
from mido import Message, MidiFile, MidiTrack

from ..entities.melody import Melody


def export_to_midi(
    melody: Melody,
    output_path: Union[str, Path],
    tempo: int = 120,
    velocity: int = 64,
    ticks_per_beat: int = 480,
) -> Path:
    """
    Экспортирует мелодию в MIDI файл.

    Args:
        melody: Мелодия для экспорта
        output_path: Путь к выходному файлу
        tempo: Темп в BPM (ударов в минуту)
        velocity: Громкость нот (0-127)
        ticks_per_beat: Разрешение MIDI файла

    Returns:
        Путь к созданному файлу
    """
    output_path = Path(output_path)

    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    microseconds_per_beat = int(60_000_000 / tempo)
    track.append(mido.MetaMessage("set_tempo", tempo=microseconds_per_beat))

    track.append(Message("program_change", program=0, time=0))

    for note in melody.notes:
        duration_ticks = int(note.duration * ticks_per_beat)

        track.append(Message("note_on", note=note.pitch, velocity=velocity, time=0))
        track.append(
            Message("note_off", note=note.pitch, velocity=0, time=duration_ticks)
        )

    track.append(mido.MetaMessage("end_of_track", time=0))

    mid.save(output_path)
    return output_path
