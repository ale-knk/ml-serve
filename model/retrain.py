import mlflow
from mlflow_utils.config import configure_mlflow
from mlflow_utils.model_io import (
    load_latest_model,
    log_model,
    register_model,
)
from model.utils import load_data, eval_model, load_config, create_pipeline_from_config
from db.client import db
from db.models import PredictionFeedback
from utils.settings import MODEL_CONFIG_PATH, MIN_IMPROVEMENT_DELTA


def retrain_if_enough_feedback(min_feedbacks: int = 10):
    configure_mlflow()

    config = load_config(MODEL_CONFIG_PATH)
    X_train, X_test, y_train, y_test = load_data(include_feedback=True)

    feedbacks = (
        db.query(PredictionFeedback)
        .filter(PredictionFeedback.used_in_retraining_run_id == None)
        .all()
    )
    if len(feedbacks) < min_feedbacks:
        print(f"Not enough feedbacks ({len(feedbacks)} < {min_feedbacks})")
        return

    current_model = load_latest_model()
    current_rmse = eval_model(current_model, X_test, y_test)

    with mlflow.start_run() as run:
        pipeline = create_pipeline_from_config(config)
        pipeline.fit(X_train, y_train)
        new_rmse = eval_model(pipeline, X_test, y_test)

        mlflow.log_metric("rmse", float(new_rmse))
        mlflow.log_param("retrain_feedbacks", len(feedbacks))
        log_model(pipeline)

        if current_rmse - new_rmse >= MIN_IMPROVEMENT_DELTA:
            print("Promoting new model to production")
            register_model(run_id=run.info.run_id, alias="production")

            for fb in feedbacks:
                fb.used_in_retraining_run_id = run.info.run_id
            db.commit()
        else:
            print("New model is not better — not promoted")


if __name__ == "__main__":
    retrain_if_enough_feedback()
