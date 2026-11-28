set dotenv-load := true
set shell := ["bash", "-uc"]

# List all recipes
default:
  @just --list


# ==========================================
# Setup commands
# ==========================================

# Run setup script
setup:
  ./scripts/setup.sh


# ==========================================
# Dev commands
# ==========================================

# Run dev server with auto-reload
[group('dev')]
dev:
  uv run fastapi dev --host 0.0.0.0 --port 8000

# Run production-like server (no reload)
[group('dev')]
run:
  uv run fastapi run --host 0.0.0.0 --port 8000



# ==========================================
# Code quality
# ==========================================

# Format and autofix
[group('quality')]
fmt:
  uv run ruff format .
  uv run ruff check --fix .

# Lint code
[group('quality')]
lint:
  uv run ruff check .

# Type check
[group('quality')]
typecheck:
  uv run mypy .


# ==========================================
# Dependencies
# ==========================================

# Add a dependency (just add requests / just add --dev pytest)
[group('deps')]
add *args:
  uv add {{args}}

# Remove a dependency
[group('deps')]
remove *args:
  uv remove {{args}}

# Sync the environment from the lockfile
[group('deps')]
sync:
  uv sync

# Upgrade all dependencies
[group('deps')]
upgrade:
  uv lock --upgrade
  uv sync


# ===========================================
# Pre-commit Hooks
# ===========================================

# Install pre-commit hooks
[group('hooks')]
pre-commit-install:
  uv run pre-commit install

# Update pre-commit hooks to latest versions
[group('hooks')]
pre-commit-update:
  uv run pre-commit autoupdate

# Run pre-commit on all files
[group('hooks')]
pre-commit-all:
  uv run pre-commit run --all-files
