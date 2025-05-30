import logging
import tempfile
from datetime import datetime

import mlflow
import numpy as np
import yaml
from api.db.client import db
from api.db.models import PredictionFeedback, PredictionLog
from api.models import (
    ModelInfoResponse,
    PredictionFeedbackRequest,
    PredictionFeedbackResponse,
    PredictionRequest,
    PredictionResponse,
)
from api.settings import MLFLOW_TRACKING_URI, MODEL_ALIAS, MODEL_NAME
from fastapi import HTTPException
from mlflow.tracking import MlflowClient

logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def get_latest_model_info() -> ModelInfoResponse:
    client = MlflowClient()
    model_version = client.get_model_version_by_alias(MODEL_NAME, MODEL_ALIAS)
    model_details = client.get_model_version(
        name=MODEL_NAME, version=model_version.version
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = client.download_artifacts(
            model_version.run_id, "config/config.yaml", tmpdir
        )
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    return ModelInfoResponse(
        name=MODEL_NAME,
        version=model_version.version,
        run_id=model_version.run_id,
        creation_time=datetime.fromtimestamp(
            model_details.creation_timestamp / 1000
        ).isoformat(),
        config=config,
    )


def load_model():
    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    logger.info(f"Loading model from URI: {model_uri}")
    model = mlflow.sklearn.load_model(model_uri)
    return model


def log_prediction(
    input_data: dict,
    prediction: float,
    model_name: str,
    model_version: str = None,
    mlflow_run_id: str = None,
    user_notes: str = None,
    extra_metadata: dict = None,
):
    log = PredictionLog(
        input_data=input_data,
        prediction=prediction,
        model_name=model_name,
        model_version=model_version,
        mlflow_run_id=mlflow_run_id,
        user_notes=user_notes,
        extra_metadata=extra_metadata,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def predict(request: PredictionRequest) -> PredictionResponse:
    logger.info(f"Received prediction request: {request}")

    model_info = get_latest_model_info()
    config = model_info.config or {}

    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    model = mlflow.sklearn.load_model(model_uri)

    input_array = np.array(
        [
            [
                request.MedInc,
                request.HouseAge,
                request.AveRooms,
                request.AveBedrms,
                request.Population,
                request.AveOccup,
                request.Latitude,
                request.Longitude,
            ]
        ]
    )

    prediction = model.predict(input_array)[0]

    log_prediction(
        input_data=request.model_dump(),
        prediction=prediction,
        model_name=MODEL_NAME,
        model_version=model_info.version,
        mlflow_run_id=model_info.run_id,
        user_notes="Prediction request",
        extra_metadata={
            "model_type": config.get("model", {}).get("type", "unknown"),
            "model_params": config.get("model", {}).get("params", {}),
            "preprocessing": config.get("preprocessing", {}),
        },
    )

    return PredictionResponse(
        prediction=prediction,
        model_name=MODEL_NAME,
        model_version=model_info.version,
        model_metadata={
            "type": config.get("model", {}).get("type", "unknown"),
            "params": config.get("model", {}).get("params", {}),
            "preprocessing": config.get("preprocessing", {}),
        },
    )


def log_feedback(request: PredictionFeedbackRequest) -> PredictionFeedbackResponse:
    prediction = (
        db.query(PredictionLog)
        .filter(PredictionLog.id == request.prediction_id)
        .first()
    )
    print("PREDICTION", prediction)
    if not prediction:
        raise HTTPException(
            status_code=404,
            detail=f"Prediction with id {request.prediction_id} not found",
        )

    feedback = PredictionFeedback(
        feedback=request.feedback,
        prediction_id=request.prediction_id,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return PredictionFeedbackResponse(
        feedback=request.feedback,
        prediction_id=request.prediction_id,
    )
