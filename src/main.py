from typing import Optional


def main(scale: Optional[str] = "C", bars: int = 4) -> None:
    """
    Главная функция приложения.

    :param scale: Тональность мелодии (например, "C", "G", "D").
    :param bars: Количество тактов.
    """
    print("Генератор мелодий запущен!")
    print(f"Тональность: {scale}")
    print(f"Длина мелодии: {bars} такта(ов)")
    print("Пока здесь только интерфейс. Логика генерации будет добавлена позже.")


if __name__ == "__main__":
    main()
