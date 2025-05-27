# MLServe

**MLServe** is a minimal ML-as-a-Service template: it exposes a machine learning model through a REST API using FastAPI, retrieves the latest production model from MLflow Model Registry, and logs predictions to a PostgreSQL database.

## 🚀 Features

* ✅ REST API with FastAPI
* ✅ Model loading from MLflow Registry
* ✅ Logging of all predictions in PostgreSQL
* ✅ Training script that registers the model in MLflow
* ✅ Dockerized infrastructure for local deployment
* ✅ Simple and clean project structure with tests

## 📦 Project Structure and Components

### API Module (`/api`)
The API module implements the REST interface using FastAPI:

* `main.py`: Application entry point and FastAPI configuration
* `routes.py`: API endpoint definitions and request handling
* `models.py`: Pydantic models for request/response validation
* `services.py`: Business logic and model serving
* `config.py`: API configuration and environment variables

### Training Module (`/training`)
Contains the model training pipeline:

* `train.py`: Training script that:
  - Loads the diabetes dataset (demo purposes)
  - Trains a Ridge regression model
  - Logs metrics and parameters to MLflow
  - Registers the model in MLflow Model Registry
  - Supports hyperparameter tuning via environment variables

### Infrastructure (`/infrastructure`)
Docker and deployment configuration:

* **Dockerfiles**:
  - `Dockerfile.api`: FastAPI application container
  - `Dockerfile.training`: Training environment container
  - `Dockerfile.mlflow`: MLflow server container

* **Docker Compose** (`docker-compose.yml`):
  - FastAPI application service
  - PostgreSQL database:
    - Used as both the prediction logging database and MLflow backend store
    - Persists data through Docker volumes
    - Initialized with custom schema for MLflow
  - MLflow tracking server:
    - Connected to PostgreSQL as backend store
    - Stores model artifacts in local volume
    - Provides model registry functionality
  - Training service

* **Database Integration**:
  - PostgreSQL serves dual purpose:
    1. Stores prediction logs from the API
    2. Acts as MLflow backend store for experiment tracking and model registry
  - MLflow is configured to use PostgreSQL with a dedicated schema
  - Database initialization handled through `init.sql`

* **Requirements**:
  - `requirements.txt`: Common dependencies
  - `requirements.api.txt`: API-specific dependencies
  - `requirements.training.txt`: Training-specific dependencies

## 🧠 Why FastAPI?
MLServe uses FastAPI as its web framework for serving predictions. The decision was made after evaluating several popular options (Flask, Django, etc.) and considering the specific needs of an ML-as-a-Service project.

FastAPI was chosen for the following reasons:

- **Speed and performance:** Built on top of Starlette and Pydantic, FastAPI provides excellent performance thanks to asynchronous request handling.

- **Type safety and validation:** FastAPI uses Python type hints and Pydantic models to automatically validate and document request and response data, reducing boilerplate code.

- **Automatic API documentation:** OpenAPI and Swagger docs are generated automatically, making it easier to explore and test the API.

- **Great fit for ML serving:** Its simplicity, speed, and data validation capabilities make it particularly well-suited for wrapping and serving machine learning models.

## ⚙️ How to Run

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (for local development)

### Quick Start
```bash
# 1. Clone repository
git clone https://github.com/yourname/predictserve.git
cd predictserve

# 2. Set up environment variables
cp .env.example .env  # Configure as needed

# 3. Launch services
docker-compose up --build

# 4. Train and register a model
python training/train.py

# 5. Make a prediction
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"feature1": 5.1, "feature2": 3.5, ...}'
```

### Services
- FastAPI: http://localhost:8000
- MLflow UI: http://localhost:5000
- PostgreSQL: localhost:5432

## 📋 TODO

* [ ] Define input schema for prediction
* [ ] Add simple authentication (optional)
* [ ] Add basic Streamlit frontend (optional)
* [ ] Add model versioning strategy
* [ ] Implement model monitoring
* [ ] Add CI/CD pipeline

## 🧑‍💻 Author

Made by Alejandro Requena – focused on building real, useful software.
