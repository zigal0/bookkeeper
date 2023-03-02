# WORK_DIR=$(shell pwd)
# export PYTHONPATH="$(WORK_DIR)" &&

# MIGRATIONS
.PHONY: local-migration-up
local-migration-up:
	echo "local migration up is processing..."
	cd bookkeeper/database && python3 migration.py up

.PHONY: local-migration-down
local-migration-down:
	echo "local migration down is processing..."
	cd bookkeeper/database && python3 migration.py down

# SETUP
.PHONY: setup
setup:
	poetry install

# TEST
.PHONY: check
check:
	poetry run pytest --cov
	poetry run mypy --strict bookkeeper
	poetry run pylint bookkeeper
	poetry run flake8 bookkeeper
