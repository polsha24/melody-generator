from ..entities.melody import Melody

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_name(pitch: int) -> str:
    octave = (pitch // 12) - 1
    name = NOTE_NAMES[pitch % 12]
    return f"{name}{octave}"


def pretty_print_melody(melody: Melody) -> str:
    """
    Красивый вывод мелодии в стиле секвенсора.
    Округляет длительности и гарантирует хотя бы один блок.
    """

    output = []
    output.append("Generated Melody")
    output.append("")

    for note in melody.notes:
        name = midi_to_name(note.pitch)

        # округление
        dur = round(note.duration, 2)

        # длина блока — 1 beat = 4 квадратика
        blocks = max(1, int(note.duration * 4))

        line = f"{name}: " + "█" * blocks + f"  ({dur} beats)"
        output.append(line)

    output.append("")
    output.append(f"Total duration: {round(melody.total_duration(), 2)} beats")

    return "\n".join(output)
