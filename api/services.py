import mlflow
from api.models import PredictionRequest, PredictionResponse, ModelInfoResponse
from api.settings import MLFLOW_TRACKING_URI, MODEL_NAME, MODEL_ALIAS
from datetime import datetime
import logging
import numpy as np
from mlflow.tracking import MlflowClient
import tempfile
import yaml

# Get logger for this module
logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def get_latest_model_info() -> ModelInfoResponse:
    client = MlflowClient()
    model_version = client.get_model_version_by_alias(MODEL_NAME, MODEL_ALIAS)
    model_details = client.get_model_version(name=MODEL_NAME, version=model_version.version)


    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = client.download_artifacts(model_version.run_id, "config/config.yaml", tmpdir)
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    return ModelInfoResponse(
        name=MODEL_NAME,
        version=model_version.version,
        run_id=model_version.run_id,
        creation_time=datetime.fromtimestamp(model_details.creation_timestamp / 1000).isoformat(),
        config=config
    )

def load_model():
    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    logger.info(f"Loading model from URI: {model_uri}")
    model = mlflow.sklearn.load_model(model_uri)
    return model

def predict(request: PredictionRequest) -> PredictionResponse:
    logger.info(f"Received prediction request: {request}")

    model_info = get_latest_model_info()
    config = model_info.config or {}

    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    model = mlflow.sklearn.load_model(model_uri)

    input_array = np.array([[
        request.MedInc,
        request.HouseAge,
        request.AveRooms,
        request.AveBedrms,
        request.Population,
        request.AveOccup,
        request.Latitude,
        request.Longitude
    ]])

    prediction = model.predict(input_array)[0]

    return PredictionResponse(
        prediction=prediction,
        model_name=MODEL_NAME,
        model_version=model_info.version,
        model_metadata={
            "type": config.get("model", {}).get("type", "unknown"),
            "params": config.get("model", {}).get("params", {}),
            "preprocessing": config.get("preprocessing", {})
        }
    )
