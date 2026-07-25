# Bloca Machine Learning Service (`bloca-ml`)

Part of the **BLOCA** ecosystem — an IoT-monitored plastic-to-brick compactor with machine learning-based grading.

`bloca-ml` is the machine learning service responsible for evaluating brick quality, processing camera imagery of compacted plastic, and analyzing anomaly detection metrics from compactor telemetry.

## Features

- **Brick Quality Grading:** AI/ML inference pipelines for classifying structural integrity and composition of recycled plastic bricks.
- **Telemetry Anomaly Detection:** Real-time analysis of pressure and temperature curves to detect compaction defects.
- **FastAPI Service:** High-performance asynchronous API endpoints for serving model predictions to backend services.

## Tech Stack

- **Language:** Python >= 3.14
- **Framework:** FastAPI
- **Dependency Management:** `uv`
- **Linting & Quality:** Ruff, Mypy, pre-commit hooks

## Project Structure

```text
bloca-ml/
├── data/              # Datasets and local storage
├── ml_models/         # Serialized model weights & artifacts
├── notebooks/         # Jupyter notebooks for experimentation
├── scripts/           # Utility & setup scripts
├── src/
│   ├── api/           # FastAPI routers and endpoints
│   ├── core/          # Configuration and core ML logic
│   ├── models/        # Data schemas and model definitions
│   ├── services/      # Inference and processing services
│   └── main.py        # Application entry point
├── tests/             # Unit and integration tests
├── pyproject.toml
└── uv.lock
```

## Related Repositories

- [`bloca-api`](https://github.com/integratech-org/bloca-api) - Backend API service
- [`bloca-firmware`](https://github.com/integratech-org/bloca-firmware) - IoT compactor firmware
