import mlflow
from utils.settings import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME

def configure_mlflow():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
