# training/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "house-price-predictor-california")
MODEL_NAME = os.getenv("MODEL_NAME", "house-price-predictor-california")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "production")
N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", 100))
MAX_DEPTH = int(os.getenv("MAX_DEPTH", 10))
