.PHONY: format lint run install-dev precommit

format:
	python -m isort src && python -m black src

lint:
	python -m ruff check src

run:
	python3 main.py

install-dev:
	python -m pip install -r requirements-dev.txt
	python -m pip install -r requirements.txt

precommit:
	pre-commit install
