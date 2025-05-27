from fastapi import APIRouter
from api.models import PredictionRequest, PredictionResponse, ModelInfoResponse
from api.services import predict, get_latest_model_info

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_route(request: PredictionRequest):
    return predict(request)

@router.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
def model_info():
    return get_latest_model_info()
