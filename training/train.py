# training/trainer.py
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import fetch_california_housing
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import yaml
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "house-price-predictor-california")
MODEL_NAME = os.getenv("MODEL_NAME", "house-price-predictor-california")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "production")
N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", 100))
MAX_DEPTH = int(os.getenv("MAX_DEPTH", 10))
CONFIG_PATH = os.getenv("MODEL_CONFIG_PATH", "training/config.yaml")


def load_config() -> dict:
    config_file = Path(CONFIG_PATH)
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

def get_model(model_config: dict):
    model_type = model_config.get("type", "").lower()
    params = model_config.get("params", {})

    if model_type == "random_forest":
        return RandomForestRegressor(**params)
    elif model_type == "gradient_boosting":
        return GradientBoostingRegressor(**params)
    elif model_type == "linear_regression":
        return LinearRegression(**params)
    else:
        raise ValueError(f"Modelo no soportado: {model_type}")

def create_pipeline(config: dict) -> Pipeline:
    steps = []
    preprocessing = config.get("preprocessing", {})

    if preprocessing.get("with_standard_scaler", False):
        steps.append(("scaler", StandardScaler()))

    if preprocessing.get("with_pca", False):
        n_components = preprocessing.get("pca_components", 5)
        steps.append(("pca", PCA(n_components=n_components)))

    model = get_model(config.get("model", {}))
    steps.append(("regressor", model))

    return Pipeline(steps)

def train_and_log_model():
    config = load_config()

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    X, y = fetch_california_housing(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    pipeline = create_pipeline(config)

    with mlflow.start_run() as run:
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        rmse = mean_squared_error(y_test, preds, squared=False)

        # Log hiperparámetros del YAML
        def log_params(prefix, d):
            for k, v in d.items():
                if isinstance(v, dict):
                    log_params(f"{prefix}.{k}", v)
                else:
                    mlflow.log_param(f"{prefix}.{k}", v)

        log_params("", config)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_artifact(CONFIG_PATH, artifact_path="config")

        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="model",
            registered_model_name=MODEL_NAME
        )


        # Asignar alias
        client = MlflowClient()
        latest_versions = client.get_latest_versions(MODEL_NAME)
        latest_version = max(int(v.version) for v in latest_versions)

        client.set_registered_model_alias(MODEL_NAME, MODEL_ALIAS, str(latest_version))

if __name__ == "__main__":
    train_and_log_model()