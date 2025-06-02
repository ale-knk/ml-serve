# settings.py
import os

from dotenv import load_dotenv

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "house-price-predictor-california")
MODEL_CONFIG_PATH = os.getenv("MODEL_CONFIG_PATH", "training/config.yaml")
RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))
MIN_IMPROVEMENT_DELTA = int(os.getenv("MIN_IMPROVEMENT_DELTA", 0.01))
MODEL_NAME = os.getenv("MODEL_NAME", "mlserve-housing-regressor")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "production")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "mlserve")
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"
)
