PYTHON = $(shell which python3.11)
SHELL = /bin/bash
VENV_DIR = .venv

DAY_TO_PY_MODULE = $(patsubst %.day,%,$@)

.PHONY: all
all: $(wildcard *.day)

%.day: install
	# Day $(DAY_TO_PY_MODULE)
	@$(VENV_DIR)/bin/python -m $(DAY_TO_PY_MODULE)

.PHONY: install
install: $(VENV_DIR)

$(VENV_DIR): requirements.txt
	@$(PYTHON) -m venv $@
	@$(VENV_DIR)/bin/python -m pip install --quiet --upgrade pip
	@$(VENV_DIR)/bin/python -m pip install --quiet --requirement=$<
	touch $@

.PHONY: lint
lint: $(VENV_DIR)
	@$</bin/python -m pip install --quiet pre-commit
	@$</bin/pre-commit install
	@$</bin/pre-commit run --all-files

.PHONY: clean
clean:
	@git clean -fdfx
