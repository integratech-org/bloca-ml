<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/integratech-org/bloca-ml">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">BLOCA ML</h3>

  <p align="center">
    Machine Learning Service for BLOCA System
    <br />
    Compressive Strength Prediction • Surface Defect Classification • Model Training
    <br />
    <a href="https://github.com/integratech-org/bloca-ml"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/integratech-org/bloca-ml/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/integratech-org/bloca-ml/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#related-projects">Related Projects</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![BLOCA ML Banner][product-banner]](https://github.com/integratech-org/bloca-ml)

**BLOCA ML** is the machine learning inference service powering quality predictions in the BLOCA ecosystem. It provides two core ML capabilities: **Random Forest regression** for predicting compressive strength (MPa) from process telemetry data, and **Convolutional Neural Network (CNN) classification** for detecting surface defects in block images.

Built with FastAPI, TensorFlow, and scikit-learn, the service exposes REST API endpoints that BLOCA Edge calls during each production batch. It loads pre-trained models from disk, performs inference with low latency, and returns predictions with confidence scores. The service is designed to run on cloud infrastructure or on-premises servers with GPU acceleration support for faster CNN inference.

Training notebooks and scripts are included in the repository for model development, hyperparameter tuning, and retraining with new production data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![FastAPI][FastAPI.com]][FastAPI-url]
* [![TensorFlow][TensorFlow.org]][TensorFlow-url]
* [![ScikitLearn][ScikitLearn.org]][ScikitLearn-url]
* [![Pandas][Pandas.org]][Pandas-url]
* [![Docker][Docker.com]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This service can be run locally for development or deployed as a containerized application.

### Prerequisites

* **Software:**
  - Python 3.12 or higher
  - [uv](https://docs.astral.sh/uv/) package manager
  - Docker and Docker Compose (for containerized deployment)

* **Optional:**
  - NVIDIA GPU with CUDA support for accelerated CNN inference
  - Jupyter Notebook for running training notebooks

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/integratech-org/bloca-ml.git
   cd bloca-ml
   ```

2. Run the setup script (installs uv and dependencies)
   ```sh
   make setup
   ```

3. Install training dependencies (optional, for model development)
   ```sh
   uv sync --group training
   ```

4. Create environment configuration
   ```sh
   cp .env.example .env
   # Edit .env with your specific configuration:
   # - Model file paths
   # - API host and port
   # - TensorFlow GPU settings (if applicable)
   ```

5. Install pre-commit hooks (for development)
   ```sh
   make pre-commit-install
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Start the ML Service

Run the FastAPI server:

```sh
uv run python -m bloca_ml
```

The service will be available at:
- **API Base**: http://localhost:8001/
- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

### Prediction Endpoints

**Compressive Strength Prediction** (Random Forest):
```sh
POST /predict/strength
Content-Type: application/json

{
  "temperature": 180.0,
  "pressure": 12.5,
  "heating_duration": 300,
  "cooling_time": 120,
  "compressed_height": 58.2,
  "power_draw": 2400
}

Response:
{
  "predicted_strength_mpa": 12.8,
  "confidence": 0.92,
  "model_version": "rf_v2.3"
}
```

**Surface Defect Classification** (CNN):
```sh
POST /predict/surface
Content-Type: multipart/form-data

image: [binary image file]

Response:
{
  "classification": "Acceptable",
  "confidence": 0.95,
  "probabilities": {
    "Acceptable": 0.95,
    "Defective": 0.04,
    "Reject": 0.01
  },
  "model_version": "cnn_v1.8"
}
```

### Model Training

Navigate to the `notebooks/` directory and open Jupyter notebooks for model training:

```sh
jupyter notebook notebooks/
```

Available notebooks:
- `01_data_exploration.ipynb` - Exploratory data analysis
- `02_strength_model_training.ipynb` - Random Forest training for compressive strength
- `03_surface_cnn_training.ipynb` - CNN training for surface defect classification
- `04_model_evaluation.ipynb` - Performance metrics and validation

Training scripts for automated workflows:
```sh
# Train Random Forest model
uv run python scripts/train_strength_model.py

# Train CNN model
uv run python scripts/train_surface_model.py

# Evaluate models
uv run python scripts/evaluate_models.py
```

### Development

Run pre-commit checks on all files:
```sh
make pre-commit-all
```

Update pre-commit hooks:
```sh
make pre-commit-update
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- FEATURES -->
## Features

### Machine Learning Models
- **Random Forest Regression**: Predicts compressive strength (MPa) from process telemetry with feature importance analysis
- **CNN Image Classification**: Classifies block surface quality into three categories (Acceptable, Defective, Reject)
- **Model Versioning**: Semantic versioning and metadata tracking for deployed models
- **Confidence Scoring**: Returns prediction confidence and class probabilities for informed decision-making

### Inference Service
- **FastAPI REST API**: High-performance async API with automatic OpenAPI documentation
- **Low-Latency Inference**: Optimized model loading and batch prediction support
- **Input Validation**: Pydantic schemas for request validation and error handling
- **Health Monitoring**: Service health checks and model readiness endpoints

### Model Training & Development
- **Jupyter Notebooks**: Interactive notebooks for data exploration and model experimentation
- **Training Scripts**: Automated training pipelines with hyperparameter tuning
- **Dataset Management**: Data versioning and train/validation/test splits in `data/` directory
- **Model Persistence**: Standardized model serialization with scikit-learn and TensorFlow SavedModel format

### Performance & Scalability
- **GPU Acceleration**: TensorFlow GPU support for faster CNN inference
- **Model Caching**: In-memory model caching to reduce load times
- **Async Processing**: Async/await pattern for concurrent request handling
- **Docker Deployment**: Containerized service with configurable resource limits

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- RELATED PROJECTS -->
## Related Projects

BLOCA ML is part of the **BLOCA (Batch-Level Optimization through Compaction Analytics)** ecosystem:

* **[bloca-edge](https://github.com/integratech-org/bloca-edge)** - IoT edge hub that calls this ML service for real-time predictions during production
* **[bloca-api](https://github.com/integratech-org/bloca-api)** - Cloud REST API backend for storing prediction results and training data
* **[bloca-admin](https://github.com/integratech-org/bloca-admin)** - Web admin dashboard for ML model auditing and retraining triggers
* **[bloca-mobile](https://github.com/integratech-org/bloca-mobile)** - Mobile application displaying prediction results to operators
* **[bloca-firmware](https://github.com/integratech-org/bloca-firmware)** - ESP32 firmware collecting the process data used for strength prediction
* **[IntegraTech Organization](https://github.com/integratech-org)** - View all BLOCA projects and documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

IntegraTech - [Facebook](https://www.facebook.com/profile.php?id=61592806334500) - integratech1@outlook.com

Project Link: [https://github.com/integratech-org/bloca-ml](https://github.com/integratech-org/bloca-ml)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/integratech-org/bloca-ml.svg?style=for-the-badge
[contributors-url]: https://github.com/integratech-org/bloca-ml/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/integratech-org/bloca-ml.svg?style=for-the-badge
[forks-url]: https://github.com/integratech-org/bloca-ml/network/members
[stars-shield]: https://img.shields.io/github/stars/integratech-org/bloca-ml.svg?style=for-the-badge
[stars-url]: https://github.com/integratech-org/bloca-ml/stargazers
[issues-shield]: https://img.shields.io/github/issues/integratech-org/bloca-ml.svg?style=for-the-badge
[issues-url]: https://github.com/integratech-org/bloca-ml/issues
[product-banner]: images/banner.png

<!-- Technology Badges -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[FastAPI.com]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[TensorFlow.org]: https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white
[TensorFlow-url]: https://www.tensorflow.org/
[ScikitLearn.org]: https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white
[ScikitLearn-url]: https://scikit-learn.org/
[Pandas.org]: https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Docker.com]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
