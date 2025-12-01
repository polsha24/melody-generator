from src.entities.scale import Scale
from src.entities.settings import GeneratorSettings
from src.services.generator import MelodyGenerator
from src.services.visualizer import pretty_print_melody


def main():
    # Создаём гамму C-мажор
    scale = Scale(root=60, intervals=[0, 2, 4, 5, 7, 9, 11])  # C4

    # Настройки генератора
    settings = GeneratorSettings(
        length=8,
        allowed_durations=[0.25, 0.5, 1.0],  # шестнадцатые, восьмые и четверти
        octave_range=1,
    )

    generator = MelodyGenerator(scale, settings)
    melody = generator.generate()

    print(pretty_print_melody(melody))


if __name__ == "__main__":
    main()
