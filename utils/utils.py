import logging

import mlflow

from utils.settings import MODEL_NAME, MODEL_ALIAS

logger = logging.getLogger(__name__)


def load_model():
    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    logger.info(f"Loading model from URI: {model_uri}")
    model = mlflow.sklearn.load_model(model_uri)
    return model
