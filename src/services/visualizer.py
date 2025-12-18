"""
Визуализация мелодий: текстовый вывод и пиано-ролл.
"""

from pathlib import Path
from typing import Optional, Union

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from ..entities.melody import Melody

NOTE_NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

FLAT_KEYS = {"F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"}


def midi_to_name(
    pitch: int,
    use_flats: bool = False,
) -> str:
    """
    Преобразует MIDI номер ноты в название.

    Args:
        pitch: MIDI номер ноты (0-127)
        use_flats: Если True, использовать бемоли (Bb), иначе диезы (A#)

    Returns:
        Название ноты, например "C4", "F#5" или "Bb3"
    """
    octave = (pitch // 12) - 1
    note_names = NOTE_NAMES_FLAT if use_flats else NOTE_NAMES_SHARP
    name = note_names[pitch % 12]
    return f"{name}{octave}"


def should_use_flats(key: str) -> bool:
    """
    Определяет, нужно ли использовать бемоли для данной тональности.

    Тональности с бемолями: F, Bb, Eb, Ab, Db, Gb
    Тональности с диезами: G, D, A, E, B, F#, C#

    Args:
        key: Название тональности

    Returns:
        True если нужны бемоли, False если диезы
    """
    return key in FLAT_KEYS


def pretty_print_melody(melody: Melody, key: str = "C") -> str:
    """
    Красивый текстовый вывод мелодии в стиле секвенсора.

    Args:
        melody: Объект мелодии
        key: Тональность для определения диезов/бемолей

    Returns:
        Форматированная строка с мелодией
    """
    use_flats = should_use_flats(key)

    output = []
    output.append("Сгенерированная мелодия")
    output.append("")

    for note in melody.notes:
        name = midi_to_name(note.pitch, use_flats=use_flats)

        dur = round(note.duration, 2)

        # 1 доля = 4 квадрата на графике
        blocks = max(1, int(note.duration * 4))

        line = f"{name}: " + "█" * blocks + f"  ({dur} долей)"
        output.append(line)

    output.append("")
    output.append(f"Общая длительность: {round(melody.total_duration(), 2)} долей")

    return "\n".join(output)


def plot_piano_roll(
    melody: Melody,
    key: str = "C",
    scale_name: str = "major",
    output_path: Optional[Union[str, Path]] = None,
    show: bool = True,
) -> Optional[Path]:
    """
    Создаёт визуализацию мелодии в виде пиано-ролла.

    Args:
        melody: Объект мелодии для визуализации
        key: Тональность для подписей нот
        scale_name: Название гаммы для заголовка
        output_path: Если указан, сохраняет график в файл
        show: Если True, отображает график

    Returns:
        Путь к сохранённому файлу, если указан output_path, иначе None
    """
    use_flats = should_use_flats(key)

    times = []
    pitches = []
    durations = []

    current_time = 0
    for note in melody.notes:
        times.append(current_time)
        pitches.append(note.pitch)
        durations.append(note.duration)
        current_time += note.duration

    min_pitch = min(pitches) - 1
    max_pitch = max(pitches) + 1

    fig, ax = plt.subplots(figsize=(12, 6))

    pitch_range = max_pitch - min_pitch if max_pitch != min_pitch else 1

    for i, (time, pitch, duration) in enumerate(zip(times, pitches, durations)):
        color = plt.cm.viridis((pitch - min_pitch) / pitch_range)
        rect = mpatches.FancyBboxPatch(
            (time, pitch - 0.4),
            duration,
            0.8,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            facecolor=color,
            edgecolor="white",
            linewidth=1.5,
        )
        ax.add_patch(rect)

    ax.set_xlim(-0.1, current_time + 0.1)
    ax.set_ylim(min_pitch - 0.5, max_pitch + 0.5)

    unique_pitches = sorted(set(pitches))
    ax.set_yticks(unique_pitches)
    ax.set_yticklabels([midi_to_name(p, use_flats) for p in unique_pitches])

    ax.set_axisbelow(True)
    ax.grid(True, axis="x", alpha=0.3, linestyle="--")
    ax.grid(True, axis="y", alpha=0.2, linestyle="-")

    ax.set_xlabel("Время (доли)", fontsize=12)
    ax.set_ylabel("Высота", fontsize=12)
    ax.set_title(f"Пиано-ролл: {key} {scale_name}", fontsize=14, fontweight="bold")

    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#16213e")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_color("#4a4a6a")

    plt.tight_layout()

    result = None
    if output_path:
        output_path = Path(output_path)
        plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor())
        result = output_path

    if show:
        plt.show()
    else:
        plt.close()

    return result
