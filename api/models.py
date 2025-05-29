# api/models.py
from pydantic import BaseModel
from typing import Dict, Any, Optional


class PredictionRequest(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


class PredictionResponse(BaseModel):
    prediction: float
    model_name: str
    model_version: str
    model_metadata: Dict[str, Any]


class ModelInfoResponse(BaseModel):
    name: str
    version: str
    run_id: str
    creation_time: str
    config: Optional[Dict[str, Any]] = None  # 🔥 añadido
