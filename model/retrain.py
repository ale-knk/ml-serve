import logging

import mlflow
from db.client import db
from db.models import PredictionFeedback
from mlflow_utils.config import configure_mlflow
from mlflow_utils.model_io import (
    load_latest_model,
    log_model,
    register_model,
)
from model.utils import eval_model, load_data
from utils.settings import MODEL_CONFIG_PATH

logger = logging.getLogger(__name__)


def retrain_if_enough_feedback(min_feedbacks: int = 10):
    logger.info("Starting retraining process")
    logger.info("Configuring MLflow")
    configure_mlflow()

    logger.info("Loading data")
    X_train, X_test, y_train, y_test = load_data(include_feedback=True)

    logger.info("Loading feedbacks")
    feedbacks = (
        db.query(PredictionFeedback)
        .filter(PredictionFeedback.retraining_run_id == None)
        .all()
    )
    if len(feedbacks) < min_feedbacks:
        logger.info(f"Not enough feedbacks ({len(feedbacks)} < {min_feedbacks})")
        return

    logger.info("Loading latest model")
    model = load_latest_model()
    logger.info("Evaluating current model")
    current_rmse = eval_model(model, X_test, y_test)

    with mlflow.start_run() as run:
        model.fit(X_train, y_train)
        new_rmse = eval_model(model, X_test, y_test)

        mlflow.log_metric("rmse", float(new_rmse))
        mlflow.log_artifact(MODEL_CONFIG_PATH, artifact_path="config")

        log_model(model)

        if new_rmse < current_rmse:
            logger.info("Promoting new model to production")
            register_model(run_id=run.info.run_id, alias="production")

            for fb in feedbacks:
                fb.retraining_run_id = run.info.run_id
            db.commit()
        else:
            logger.info("New model is not better — not promoted")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    retrain_if_enough_feedback()
