from src.entities.scale import NOTE_TO_MIDI, Scale, ScaleType
from src.entities.settings import GeneratorSettings
from src.services.exporter import export_to_midi
from src.services.generator import MelodyGenerator
from src.services.player import play_midi
from src.services.visualizer import plot_piano_roll, pretty_print_melody


def get_valid_input(prompt: str, valid_options: list, default: str = None) -> str:
    """Get validated input from user with optional default."""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}: ").strip()

        # Case-insensitive matching
        for option in valid_options:
            if user_input.lower() == option.lower():
                return option

        print(f"  Invalid choice. Options: {', '.join(valid_options)}")


def get_int_input(
    prompt: str, default: int, min_val: int = 1, max_val: int = 999
) -> int:
    """Get validated integer input from user."""
    while True:
        user_input = input(f"{prompt} [{default}]: ").strip()
        if not user_input:
            return default

        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"  Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("  Please enter a valid number")


def interactive_input() -> dict:
    """Collect melody parameters interactively."""
    print("\n" + "=" * 50)
    print("       MELODY GENERATOR")
    print("=" * 50)
    print("\nPress Enter to use default values shown in [brackets]\n")

    # Available options
    available_keys = sorted(set(NOTE_TO_MIDI.keys()))
    available_scales = [s.value for s in ScaleType]

    # Key (root note)
    print(f"Available keys: {', '.join(available_keys)}")
    key = get_valid_input("Key (root note)", available_keys, default="C")
    print()

    # Scale type
    print(f"Available scales: {', '.join(available_scales)}")
    scale = get_valid_input("Scale type", available_scales, default="major")
    print()

    # Length
    length = get_int_input("Number of notes (1-64)", default=8, min_val=1, max_val=64)

    # Tempo
    tempo = get_int_input("Tempo in BPM (40-300)", default=120, min_val=40, max_val=300)

    # Octave range
    octave_range = get_int_input(
        "Octave range +/- (0-3)", default=0, min_val=0, max_val=3
    )

    # Output file
    output = input("Output file [output.mid]: ").strip() or "output.mid"
    if not output.endswith(".mid"):
        output += ".mid"

    # Visualization
    show_viz = get_valid_input(
        "Show piano roll visualization? (yes/no)", ["yes", "no"], default="yes"
    )

    # Play melody
    play_melody = get_valid_input("Play melody? (yes/no)", ["yes", "no"], default="yes")

    print()
    return {
        "key": key,
        "scale": scale,
        "length": length,
        "tempo": tempo,
        "octave_range": octave_range,
        "output": output,
        "show_visualization": show_viz == "yes",
        "play_melody": play_melody == "yes",
    }


def main():
    # Get parameters interactively
    params = interactive_input()

    # Create scale
    scale_type = ScaleType(params["scale"])
    scale = Scale.from_key(params["key"], scale_type)

    # Generator settings
    settings = GeneratorSettings(
        length=params["length"],
        allowed_durations=[0.25, 0.5, 1.0],
        octave_range=params["octave_range"],
    )

    # Generate melody
    generator = MelodyGenerator(scale, settings)
    melody = generator.generate()

    # Display results
    print("=" * 50)
    print(f"Key: {params['key']} {params['scale']}")
    print(f"Tempo: {params['tempo']} BPM")
    print(f"Notes: {params['length']}")
    print("=" * 50 + "\n")

    print(pretty_print_melody(melody, key=params["key"]))

    # Export to MIDI
    output_file = export_to_midi(melody, params["output"], tempo=params["tempo"])
    print(f"\nMIDI file saved to: {output_file}")

    # Show visualization
    if params["show_visualization"]:
        # Save image alongside MIDI
        image_path = params["output"].replace(".mid", ".png")
        plot_piano_roll(
            melody,
            key=params["key"],
            scale_name=params["scale"],
            output_path=image_path,
            show=True,
        )
        print(f"Piano roll saved to: {image_path}")

    # Play melody
    if params["play_melody"]:
        print("\nPlaying melody... (close to stop)")
        play_midi(output_file, wait=True)
        print("Playback finished.")


if __name__ == "__main__":
    main()
