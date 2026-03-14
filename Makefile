SHELL := /bin/sh

UV ?= uv
DOCKER_COMPOSE ?= docker compose
PYTEST_PATHS ?= src tests
MESSAGE ?=
REVISION ?= -1

.DEFAULT_GOAL := help

.PHONY: help install install-dev run lint format typecheck test check pre-commit lock lock-upgrade db-up db-down db-logs migrate downgrade revision

help: ## Show available commands
	@awk 'BEGIN {FS = ": ## "}; /^[a-zA-Z0-9_.-]+: ## / {printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install runtime dependencies
	$(UV) sync --no-dev

install-dev: ## Install runtime and development dependencies
	$(UV) sync

run: ## Run the bot
	$(UV) run bot-run

lint: ## Run Ruff checks
	$(UV) run ruff check src

format: ## Format the codebase with Ruff
	$(UV) run ruff format src

typecheck: ## Run ty type checks
	$(UV) run ty check src

test: ## Run pytest if tests exist
	@if find $(PYTEST_PATHS) -type f \( -name 'test_*.py' -o -name '*_test.py' \) 2>/dev/null | grep -q .; then \
		$(UV) run pytest; \
	else \
		echo "No tests found."; \
	fi

check: ## Run linting, type checks, and tests
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test

pre-commit: ## Run all pre-commit hooks
	$(UV) run pre-commit run --all-files

lock: ## Refresh the lock file
	$(UV) lock

lock-upgrade: ## Upgrade dependencies and refresh the lock file
	$(UV) lock --upgrade

db-up: ## Start local services from compose
	$(DOCKER_COMPOSE) up -d

db-down: ## Stop local services from compose
	$(DOCKER_COMPOSE) down

db-logs: ## Tail compose service logs
	$(DOCKER_COMPOSE) logs -f

migrate: ## Apply all Alembic migrations
	$(UV) run alembic upgrade head

downgrade: ## Roll back Alembic migrations, use REVISION=<target>
	$(UV) run alembic downgrade $(REVISION)

revision: ## Create an Alembic revision, use MESSAGE=<name>
	@test -n "$(MESSAGE)" || (echo "Usage: make revision MESSAGE=add_users_table" && exit 1)
	$(UV) run alembic revision --autogenerate -m "$(MESSAGE)"
