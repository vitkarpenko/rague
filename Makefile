test:
	python -m pytest tests

format:
	isort . -rc
	black .

check:
	flake8
	isort --check --diff
	black . --check --diff