ci:
	ruff format
	ruff check --fix


.PHONY: tests
tests:
	ENV=TEST pytest --cov=src
