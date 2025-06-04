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
from utils.settings import MIN_IMPROVEMENT_DELTA


def retrain_if_enough_feedback(min_feedbacks: int = 10):
    print("Retraining if enough feedback")
    print("Configuring MLflow")
    configure_mlflow()

    print("Loading data")
    X_train, X_test, y_train, y_test = load_data(include_feedback=True)

    print("Loading feedbacks")
    feedbacks = (
        db.query(PredictionFeedback)
        .filter(PredictionFeedback.used_in_retraining_run_id == None)
        .all()
    )
    if len(feedbacks) < min_feedbacks:
        print(f"Not enough feedbacks ({len(feedbacks)} < {min_feedbacks})")
        return

    print("Loading latest model")
    model = load_latest_model()
    print("Evaluating current model")
    current_rmse = eval_model(model, X_test, y_test)

    with mlflow.start_run() as run:
        model.fit(X_train, y_train)
        new_rmse = eval_model(model, X_test, y_test)

        mlflow.log_metric("rmse", float(new_rmse))
        mlflow.log_param("retrain_feedbacks", len(feedbacks))
        log_model(model)

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
