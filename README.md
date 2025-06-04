# MLServe

**MLServe** is a minimal ML-as-a-Service template: it exposes a machine learning model through a REST API using FastAPI, retrieves the latest production model from MLflow Model Registry, logs predictions to a PostgreSQL database, implements functionality to collect prediction feedback, and includes cron jobs for model retraining based on the collected feedback.

## 🚀 Features

*   ✅ **REST API with FastAPI:** Exposes the ML model with well-defined routes and automatic data validation.
*   ✅ **Automatic model loading from MLflow:** Fetching the latest production version from MLflow Model Registry to ensure consistent deployments.

*   ✅ **Prediction logging in PostgreSQL:** All requests and results are stored in a relational database for auditing and usage analysis.

*   ✅ **Artifact storage in MINIO (S3-compatible):** Managed MLflow artifacts locally with an easy path to migrate to AWS S3.

*   ✅ **Feedback system for continuous improvement:** Capture user feedback on predictions, enabling model refinement.

*   ✅ **Automated retraining pipeline:** Scheduled tasks (cron jobs) that collect feedback, retrain the model, and register new versions in MLflow without manual intervention.

*   ✅ **Dockerized containers for reproducible local deployment:** Isolated images for API, training, MLflow, database, and MINIO, orchestrated via Docker Compose.

*   ✅ **Modular, maintainable architecture:** Clear separation between API layer, business logic, data management, and training module, facilitating extensions and testing.


## ⚙️ How to Run

### Prerequisites

*   Docker and Docker Compose

*   Python 3.12+

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourname/ml-serve.git
cd ml-serve

# 2. Set up environment variables
cp .env.example .env  # Configure as needed

# 3. Launch services
make up # This can take a while for the first time

# 4. Get info about latest model
curl -X GET http://localhost:8000/model-info

# 5. Make a prediction
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{
       "MedInc": 6.5,
       "HouseAge": 30.0,
       "AveRooms": 5.8,
       "AveBedrms": 1.1,
       "Population": 850.0,
       "AveOccup": 2.8,
       "Latitude": 34.12,
       "Longitude": -118.35
     }'

# 6. Send feedback
curl -X POST http://localhost:8000/feedback \
     -H "Content-Type: application/json" \
     -d '{
       "prediction_id": 1,
       "feedback":1.4
     }' 


# (OPTIONAL) For checking retraining activities
python scripts/simulate_activity.py #This will send some predictions and feedback
docker logs retrain #Logs will inform about retraining status.
```


## 📦 Project Structure and Components

### API Module (`/api`)

The API module implements the REST interface using FastAPI:

*   `main.py`: Application entry point and FastAPI configuration
*   `routes.py`: API endpoint definitions and request handling
*   `models.py`: Pydantic models for request/response validation
*   `services.py`: Business logic and model serving
*   `settings.py`: API configuration and environment variables

### Model Module (`/model`)

Contains the model training and retraining pipeline:

*   `train.py`: Training script that:
    *   Loads the California Housing dataset from scikit-learn
    *   Trains a Ridge regression model
    *   Logs metrics and parameters to MLflow
    *   Registers the model in MLflow Model Registry
    *   Supports hyperparameter tuning via environment variables
*   `retrain.py`: Retraining script that:
    *   Loads feedback data from the database
    *   Retrains the model using the collected feedback
    *   Updates the model in MLflow Registry
*   `utils.py`: Helper functions for model operations
*   `model_config.yaml`: Model configuration and hyperparameters

### Database Module (`/db`)

Database integration and models:

*   `models.py`: SQLAlchemy models for database tables
*   `client.py`: Database connection and session management
*   `__main__.py`: Database initialization and setup

### MLflow Utilities (`/mlflow_utils`)

MLflow integration and helper functions:

*   Model registry operations
*   Experiment tracking utilities
*   Model versioning helpers

### Infrastructure (`/infra`)

Docker and deployment configuration:

*   **Dockerfiles and Services**:
    *   `api/`: FastAPI application container and requirements
    *   `train/`: Training environment container and requirements
    *   `mlflow/`: MLflow server container
    *   `init-db/`: Database initialization container with entrypoint script
    *   `postgres/`: PostgreSQL configuration and initialization scripts

*   **Docker Compose** (`docker-compose.yml`):
    *   FastAPI application service
    *   PostgreSQL database:
        *   Used as both the prediction logging database and MLflow backend store
        *   Persists data through Docker volumes
        *   Initialized with custom schema for MLflow
    *   MLflow tracking server:
        *   Connected to PostgreSQL as backend store
        *   Stores model artifacts in MINIO (S3-compatible storage)
        *   Provides model registry functionality
    *   MINIO object storage:
        *   S3-compatible storage for MLflow artifacts
        *   Perfect for local development and testing
        *   Seamless transition to AWS S3 in production
    *   Training service
    *   Retraining service (CRON Job)
    *   Database initialization service

*   **Storage Integration**:
    *   MINIO is used as the artifact storage backend for MLflow
    *   Provides S3-compatible API, making it ideal for development
    *   Easy transition to AWS S3 in production by updating environment variables
    *   Stores model artifacts, experiment data, and other binary files
    *   Accessible through the MINIO UI for easy artifact management

*   **Database Integration**:
    *   PostgreSQL serves dual purpose:
        1. Stores prediction logs from the API
        2. Acts as MLflow backend store for experiment tracking and model registry
    *   MLflow is configured to use PostgreSQL with a dedicated schema
    *   Database initialization handled through `postgres/init.sql`
    *   Database initialization service with custom entrypoint script

*   **Requirements**:
    *   `api/requirements.txt`: API-specific dependencies
    *   `train/requirements.txt`: Training-specific dependencies
    *   `init-db/requirements.txt`: Database initialization dependencies

### Utils Module (`/utils`)

Common utilities and helper functions used across the project:

*   Data processing utilities
*   Logging helpers
*   Common configuration management
*   Shared type definitions

## 🧠 Why FastAPI?

MLServe uses FastAPI as its web framework for serving predictions. The decision was made after evaluating several popular options (Flask, Django, etc.) and considering the specific needs of an ML-as-a-Service project.

FastAPI was chosen for the following reasons:

*   **Speed and performance:** Built on top of Starlette and Pydantic, FastAPI provides excellent performance thanks to asynchronous request handling.

*   **Type safety and validation:** FastAPI uses Python type hints and Pydantic models to automatically validate and document request and response data, reducing boilerplate code.

*   **Automatic API documentation:** OpenAPI and Swagger docs are generated automatically, making it easier to explore and test the API.

*   **Great fit for ML serving:** Its simplicity, speed, and data validation capabilities make it particularly well-suited for wrapping and serving machine learning models.

### Services

Given the `.env.example` file, once services are up, you can navigate into:
*   **FastAPI:** <http://localhost:8000>

*   **MLflow UI:** <http://localhost:5555>
*   **PGAdmin UI:** <http://localhost:5500>
*   **MINIO UI:** <http://localhost:9001>

## 📋 TODO

*   [ ] Add comprehensive API documentation
*   [ ] Implement model versioning strategy
*   [ ] Add model monitoring and drift detection
*   [ ] Add CI/CD pipeline
*   [ ] Add integration tests


## 🧑‍💻 Author

Made by Alejandro Requena – focused on building real, useful software.
