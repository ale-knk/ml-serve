from api.models import ModelInfoResponse, PredictionFeedbackRequest, PredictionFeedbackResponse, PredictionRequest, PredictionResponse
from api.services import get_latest_model_info, log_feedback, predict
from fastapi import APIRouter

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_route(request: PredictionRequest):
    return predict(request)


@router.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
def model_info():
    return get_latest_model_info()


@router.post("/feedback", response_model=PredictionFeedbackResponse, tags=["Feedback"])
def feedback(request: PredictionFeedbackRequest):
    return log_feedback(request)