.PHONY: format lint run install-dev precommit

format:  # запускайте лучше через `poetry run`, раз подключили Poetry
	python -m isort src && python -m black src

lint:  # запускайте лучше через `poetry run`, раз подключили Poetry
	python -m ruff check src

run:
	python3 main.py

install-dev:  # не работает (нет requirements-dev.txt)
	python -m pip install -r requirements-dev.txt
	python -m pip install -r requirements.txt

precommit:
	pre-commit install
