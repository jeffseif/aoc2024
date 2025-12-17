SHELL = /bin/bash
MODULE_NAME = $(shell basename $(PWD))

.PHONY: all
all:
	uv run --no-dev python -m $(MODULE_NAME)

.PHONY: lint
lint:
	@uv run --dev pre-commit run --all-files

.PHONY: clean
clean:
	@git clean -fdfx
