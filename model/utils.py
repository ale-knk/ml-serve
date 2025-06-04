from pathlib import Path

import yaml
from sklearn.datasets import fetch_california_housing
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from db.models import PredictionFeedback, PredictionLog
from sklearn.metrics import mean_squared_error
import pandas as pd
from db.client import db
import json
from sklearn.model_selection import train_test_split
from utils.settings import RANDOM_SEED


def get_unused_feedback():
    return (
        db.query(PredictionFeedback)
        .filter(PredictionFeedback.used_in_retraining_run_id == None)
        .all()
    )

def load_config(config_path: str) -> dict:
    config_file = Path(config_path)
    with open(config_file, "r") as f:
        return yaml.safe_load(f)
    
def load_base_data():
    data = fetch_california_housing(as_frame=True)
    X = data.data
    y = data.target
    return X, y

def get_feedback_data():
    query = (
        db.query(PredictionLog.input_data, PredictionFeedback.feedback)
        .join(PredictionFeedback, PredictionLog.id == PredictionFeedback.prediction_id)
        .filter(PredictionFeedback.retraining_run_id == None)
    )

    rows = query.all()

    input_dicts = [
        json.loads(row[0]) if isinstance(row[0], str) else row[0] for row in rows
    ]
    feedback_values = [row[1] for row in rows]

    X_fb = pd.DataFrame(input_dicts)
    y_fb = pd.Series(feedback_values)

    return X_fb, y_fb

def load_data(include_feedback: bool = False):
    X_base, y_base = load_base_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X_base, y_base, test_size=0.2, random_state=RANDOM_SEED
    )

    if include_feedback:
        X_fb, y_fb = get_feedback_data()

        X_train = pd.concat([X_train, X_fb], axis=0)
        y_train = pd.concat([y_train, y_fb], axis=0)

    return X_train, X_test, y_train, y_test

def build_model_from_config(model_config: dict):
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

def create_pipeline_from_config(config: dict) -> Pipeline:
    steps = []
    preprocessing = config.get("preprocessing", {})

    if preprocessing.get("with_standard_scaler", False):
        steps.append(("scaler", StandardScaler()))

    if preprocessing.get("with_pca", False):
        n_components = preprocessing.get("pca_components", 5)
        steps.append(("pca", PCA(n_components=n_components)))

    model = build_model_from_config(config.get("model", {}))
    steps.append(("regressor", model))

    return Pipeline(steps)

def eval_model(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series):
    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    return rmse
