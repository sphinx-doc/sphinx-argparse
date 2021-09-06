.PHONY: help init build test lint pretty precommit_install bump_major bump_minor bump_patch

BIN = .venv/bin/
CODE = sphinxarg

help: # Make help to show possible targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init:  ## Create a virtualenv for dev
	python3 -m venv .venv
	.venv/bin/pip install -U pip setuptools
	poetry install

build:  ## Build the sdist/wheel packages
	poetry build

test:  ## Test the project
	poetry run pytest --verbosity=2 --log-level=DEBUG $(args)

lint:  ## Check code for style
	pre-commit run
	poetry run pytest --dead-fixtures --dup-fixtures

pretty: ## Prettify the code
	poetry run isort $(CODE) test/
	poetry run black $(CODE) test/

precommit_install: ## Install simple pre-commit checks
	pre-commit install

bump_major: ## Release a new major version
	poetry version major

bump_minor: ## Release a new minor version
	poetry version minor

bump_patch: ## Release a new patch version
	poetry version patch
