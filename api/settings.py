# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "mlserve-housing-regressor")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "production")
