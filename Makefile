# WORK_DIR=$(shell pwd)
# export PYTHONPATH="$(WORK_DIR)" &&

# MIGRATIONS
.PHONY: local-migration-up
local-migration-up:
	echo "Local migration up is processing..."
	cd bookkeeper/database && poetry run python3 migration.py up

.PHONY: local-migration-down
local-migration-down:
	echo "Local migration down is processing..."
	cd bookkeeper/database && poetry run python3 migration.py down

.PHONY: local-migration-rs
local-migration-rs:
	make local-migration-down
	make local-migration-up

# SETUP
.PHONY: setup
setup:
	poetry install

# CHECK
.PHONY: lint
lint:
	poetry run mypy --strict bookkeeper
	poetry run pylint bookkeeper
	poetry run flake8 bookkeeper

.PHONY: test
test:
	poetry run pytest --cov

.PHONY: check
check:
	make test
	make lint


# RUN
.PHONY: run
run:
	echo "Running app..."
	poetry run python3 bookkeeper/simple_client.py

.PHONY: run-full
run-full:
	make local-migration-rs
	cd bookkeeper && poetry run python3 simple_client.py


