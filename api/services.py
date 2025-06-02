import logging
import tempfile
from datetime import datetime

import mlflow
import numpy as np
import yaml

from db.client import db
from db.models import PredictionFeedback, PredictionLog

from mlflow_utils.model_io import load_latest_model_info, load_latest_model
from api.models import (
    ModelInfoResponse,
    PredictionFeedbackRequest,
    PredictionFeedbackResponse,
    PredictionRequest,
    PredictionResponse,
)
from api.settings import MLFLOW_TRACKING_URI, MODEL_ALIAS, MODEL_NAME
from fastapi import HTTPException

logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def get_latest_model_info() -> ModelInfoResponse:
    model_info = load_latest_model_info()
    return ModelInfoResponse(**model_info)


def log_prediction(
    input_data: dict,
    prediction: float,
    model_name: str,
    model_version: str,
    mlflow_run_id: str,
    user_notes: str,
    extra_metadata: dict,
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

    model_info = load_latest_model_info()
    config = model_info["config"] or {}

    model = load_latest_model()

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
        model_version=model_info["version"],
        mlflow_run_id=model_info["run_id"],
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
        model_version=model_info["version"],
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
