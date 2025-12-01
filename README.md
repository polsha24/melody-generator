# Melody Generator

Проект для генерации простой музыкальной мелодии на основе заданной тональности, количества тактов и темпа.

## Цель проекта

Создать инструмент, который позволит программно формировать музыкальные последовательности и сохранять их для последующего прослушивания или анализа.

## Структура проекта

```
melody-generator/
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── .pre-commit-config.yaml
├── Makefile
├── src/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── note.py
│   │   ├── scale.py
│   │   ├── melody.py
│   │   └── settings.py
│   └── services/
│       ├── __init__.py
│       ├── generator.py
│       ├── exporter.py
│       └── visualizer.py
└── tests/
	└── (здесь будут тесты)
```

## Статус

На текущем этапе реализованы:

- Описание основных структур данных
- Базовая модель данных для ноты, гаммы и мелодии
- Начальная версия точки входа `main.py`

Дальнейшие шаги:

- Реализовать логику генерации мелодии в `MelodyGenerator`
- Добавить экспорт в MIDI
- Добавить визуализацию мелодии
- Добавить FastAPI

## Developer setup

Рекомендуется использовать виртуальное окружение для разработки.

1. Создать и активировать виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Установить runtime зависимости и инструменты разработки:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Установить git-хуки `pre-commit`:

```bash
pre-commit install
```

Полезные команды (из корня проекта):

```bash
make format   # Запустить isort + black
make lint     # Запустить ruff
make run      # Запустить main.py
```


## Автор

Токунова Полина, 22ФПЛ1
