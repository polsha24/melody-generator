from src.entities.note import Note
from src.entities.scale import Scale
from src.entities.melody import Melody
from src.services.generator import MelodyGenerator


def main():
    """
    Точка входа программы
    (на данном этапе просто демонстрирует работу базовых сущностей)
    """

    # Создаем гамму (пока просто список MIDI нот)
    scale = Scale(name="C major", notes=[60, 62, 64, 65, 67, 69, 71, 72])

    # Создаем генератор мелодии (логика появится позже)
    generator = MelodyGenerator(scale=scale, bars=4, tempo=120)

    # Пока генератор не реализован, создадим мелодию вручную
    melody = Melody(
        notes=[
            Note(name="C", midi=60, duration=1.0),
            Note(name="D", midi=62, duration=1.0),
            Note(name="E", midi=64, duration=1.0),
        ],
        tempo=120,
        bars=4
    )

    print("Гамма:", scale)
    print("Мелодия:", melody)


if __name__ == "__main__":
    main()
