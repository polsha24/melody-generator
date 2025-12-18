from pathlib import Path
from typing import Optional, Union

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from ..entities.melody import Melody

NOTE_NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

# Keys that traditionally use flats
FLAT_KEYS = {"F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb", "D", "G", "A", "E", "B"}


def midi_to_name(
    pitch: int,
    use_flats: bool = False,
) -> str:
    """
    Convert MIDI pitch to note name.

    Args:
        pitch: MIDI note number (0-127)
        use_flats: If True, use flats (Bb), otherwise sharps (A#)

    Returns:
        Note name like "C4", "F#5", or "Bb3"
    """
    octave = (pitch // 12) - 1
    note_names = NOTE_NAMES_FLAT if use_flats else NOTE_NAMES_SHARP
    name = note_names[pitch % 12]
    return f"{name}{octave}"


def should_use_flats(key: str) -> bool:
    """
    Determine if a key should use flat notation.

    Keys with flats in their signature: F, Bb, Eb, Ab, Db, Gb
    Keys with sharps in their signature: G, D, A, E, B, F#, C#
    """
    flat_keys = {"F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"}
    return key in flat_keys


def pretty_print_melody(melody: Melody, key: str = "C") -> str:
    """
    Красивый вывод мелодии в стиле секвенсора.
    Округляет длительности и гарантирует хотя бы один блок.

    Args:
        melody: Melody object
        key: Key name to determine sharp/flat notation
    """
    use_flats = should_use_flats(key)

    output = []
    output.append("Generated Melody")
    output.append("")

    for note in melody.notes:
        name = midi_to_name(note.pitch, use_flats=use_flats)

        # округление
        dur = round(note.duration, 2)

        # длина блока — 1 beat = 4 квадратика
        blocks = max(1, int(note.duration * 4))

        line = f"{name}: " + "█" * blocks + f"  ({dur} beats)"
        output.append(line)

    output.append("")
    output.append(f"Total duration: {round(melody.total_duration(), 2)} beats")

    return "\n".join(output)


def plot_piano_roll(
    melody: Melody,
    key: str = "C",
    scale_name: str = "major",
    output_path: Optional[Union[str, Path]] = None,
    show: bool = True,
) -> Optional[Path]:
    """
    Create a piano roll visualization of the melody.

    Args:
        melody: Melody object to visualize
        key: Key name for note labeling
        scale_name: Scale name for the title
        output_path: If provided, save the plot to this file
        show: If True, display the plot

    Returns:
        Path to saved file if output_path provided, else None
    """
    use_flats = should_use_flats(key)

    # Prepare data
    times = []
    pitches = []
    durations = []

    current_time = 0
    for note in melody.notes:
        times.append(current_time)
        pitches.append(note.pitch)
        durations.append(note.duration)
        current_time += note.duration

    # Get pitch range for Y axis
    min_pitch = min(pitches) - 1
    max_pitch = max(pitches) + 1

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Color gradient based on pitch (normalize to 0-1 range)
    pitch_range = max_pitch - min_pitch if max_pitch != min_pitch else 1

    # Draw notes as rectangles
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

    # Configure axes
    ax.set_xlim(-0.1, current_time + 0.1)
    ax.set_ylim(min_pitch - 0.5, max_pitch + 0.5)

    # Y-axis: show note names
    unique_pitches = sorted(set(pitches))
    ax.set_yticks(unique_pitches)
    ax.set_yticklabels([midi_to_name(p, use_flats) for p in unique_pitches])

    # Grid
    ax.set_axisbelow(True)
    ax.grid(True, axis="x", alpha=0.3, linestyle="--")
    ax.grid(True, axis="y", alpha=0.2, linestyle="-")

    # Labels
    ax.set_xlabel("Time (beats)", fontsize=12)
    ax.set_ylabel("Pitch", fontsize=12)
    ax.set_title(f"Piano Roll: {key} {scale_name}", fontsize=14, fontweight="bold")

    # Style
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#16213e")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_color("#4a4a6a")

    plt.tight_layout()

    # Save if path provided
    result = None
    if output_path:
        output_path = Path(output_path)
        plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor())
        result = output_path

    # Show plot
    if show:
        plt.show()
    else:
        plt.close()

    return result
