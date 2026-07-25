# Setup Guide — Bloca ML Service (`bloca-ml`)

Follow these instructions to set up, run, and develop the `bloca-ml` service locally.

## Prerequisites

- **Python**: Version 3.14 or higher
- **Package Manager**: `uv`
- **Make**: (optional) For running Makefile shortcuts

## Installation & Setup

1. Navigate to the project directory:
   ```bash
   cd bloca-ml
   ```

2. Run the development environment setup. This checks requirements and configures pre-commit hooks:
   ```bash
   make setup
   # or run the script directly:
   ./scripts/setup.sh
   ```

3. Install python dependencies using `uv`:
   ```bash
   uv sync
   ```

## Running the Development Server

Start the FastAPI development server with auto-reload:

```bash
uv run uvicorn src.main:app --reload
```

The service will be available at `http://localhost:8000` (with OpenAPI docs at `/docs`).

## Code Quality, Testing & Pre-commit

- **Pre-commit Hooks Management (via Makefile):**
  - Install pre-commit hooks manually:
    ```bash
    make pre-commit-install
    ```
  - Run pre-commit checks on all files:
    ```bash
    make pre-commit-all
    ```
  - Update pre-commit hooks to their latest versions:
    ```bash
    make pre-commit-update
    ```

- **Manual Code Quality & Verification:**
  - **Linting (Ruff):**
    ```bash
    uv run ruff check .
    ```
  - **Type Checking (Mypy):**
    ```bash
    uv run mypy src/
    ```
  - **Running Tests:**
    ```bash
    pytest
    ```
