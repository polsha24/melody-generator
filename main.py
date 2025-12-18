"""
Консольный интерфейс генератора мелодий.
"""

from src.entities.scale import NOTE_TO_MIDI, Scale, ScaleType
from src.entities.settings import GeneratorSettings
from src.services.exporter import export_to_midi
from src.services.generator import MelodyGenerator
from src.services.player import play_midi
from src.services.visualizer import plot_piano_roll, pretty_print_melody


def get_valid_input(prompt: str, valid_options: list, default: str = None) -> str:
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}: ").strip()

        # Сравнение без учёта регистра
        for option in valid_options:
            if user_input.lower() == option.lower():
                return option

        print(f"  Неверный выбор. Доступные варианты: {', '.join(valid_options)}")


def get_int_input(
    prompt: str, default: int, min_val: int = 1, max_val: int = 999
) -> int:
    """Получение валидированного целочисленного ввода от пользователя."""
    while True:
        user_input = input(f"{prompt} [{default}]: ").strip()
        if not user_input:
            return default

        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"  Введите число от {min_val} до {max_val}")
        except ValueError:
            print("  Введите корректное число")


def interactive_input() -> dict:
    """Интерактивный сбор параметров мелодии."""
    print("\n" + "=" * 50)
    print("       ГЕНЕРАТОР МЕЛОДИЙ")
    print("=" * 50)
    print("\nНажмите Enter для значений по умолчанию [в скобках]\n")

    # Доступные опции
    available_keys = sorted(set(NOTE_TO_MIDI.keys()))
    available_scales = [s.value for s in ScaleType]

    # Тональность
    print(f"Доступные тональности: {', '.join(available_keys)}")
    key = get_valid_input("Тональность", available_keys, default="C")
    print()

    # Тип гаммы
    print(f"Доступные гаммы: {', '.join(available_scales)}")
    scale = get_valid_input("Тип гаммы", available_scales, default="major")
    print()

    # Количество нот
    length = get_int_input("Количество нот (1-64)", default=8, min_val=1, max_val=64)

    # Темп
    tempo = get_int_input("Темп в BPM (40-300)", default=120, min_val=40, max_val=300)

    # Диапазон октав
    octave_range = get_int_input(
        "Диапазон октав +/- (0-3)", default=0, min_val=0, max_val=3
    )

    # Выходной файл
    output = input("Имя файла [output.mid]: ").strip() or "output.mid"
    if not output.endswith(".mid"):
        output += ".mid"

    # Визуализация
    show_viz = get_valid_input(
        "Показать пиано-ролл? (yes/no)", ["yes", "no"], default="yes"
    )

    # Воспроизведение
    play_melody = get_valid_input(
        "Воспроизвести мелодию? (yes/no)", ["yes", "no"], default="yes"
    )

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
    """Основная функция программы."""
    # Получаем параметры интерактивно
    params = interactive_input()

    # Создаём гамму
    scale_type = ScaleType(params["scale"])
    scale = Scale.from_key(params["key"], scale_type)

    # Настройки генератора
    settings = GeneratorSettings(
        length=params["length"],
        allowed_durations=[0.25, 0.5, 1.0],
        octave_range=params["octave_range"],
    )

    # Генерируем мелодию
    generator = MelodyGenerator(scale, settings)
    melody = generator.generate()

    # Выводим результаты
    print("=" * 50)
    print(f"Тональность: {params['key']} {params['scale']}")
    print(f"Темп: {params['tempo']} BPM")
    print(f"Нот: {params['length']}")
    print("=" * 50 + "\n")

    print(pretty_print_melody(melody, key=params["key"]))

    # Экспорт в MIDI
    output_file = export_to_midi(melody, params["output"], tempo=params["tempo"])
    print(f"\nMIDI файл сохранён: {output_file}")

    # Показываем визуализацию
    if params["show_visualization"]:
        # Сохраняем изображение рядом с MIDI
        image_path = params["output"].replace(".mid", ".png")
        plot_piano_roll(
            melody,
            key=params["key"],
            scale_name=params["scale"],
            output_path=image_path,
            show=True,
        )
        print(f"Пиано-ролл сохранён: {image_path}")

    # Воспроизводим мелодию
    if params["play_melody"]:
        print("\nВоспроизведение мелодии...")
        play_midi(output_file, wait=True)
        print("Воспроизведение завершено.")


if __name__ == "__main__":
    main()
