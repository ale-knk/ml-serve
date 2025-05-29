# api/models.py
from pydantic import BaseModel
from typing import Dict, Any, Optional
from sqlalchemy import Column, Integer, Text, DateTime, JSON, func
from api.db import Base

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

class PredictionLog(Base):
    __tablename__ = 'prediction_logs'
    __table_args__ = {'schema': 'predictions'}

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    input_data = Column(JSON, nullable=False)
    prediction_result = Column(JSON, nullable=False)
    model_name = Column(Text, nullable=False)
    model_version = Column(Text)
    mlflow_run_id = Column(Text)
    user_notes = Column(Text)
    extra_metadata = Column(JSON)