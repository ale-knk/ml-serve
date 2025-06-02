import mlflow
import mlflow.sklearn
# from dotenv import load_dotenv
from mlflow_utils.config import configure_mlflow
from mlflow_utils.model_io import log_model, register_model
from utils.settings import MODEL_CONFIG_PATH
from model.utils import load_config, create_pipeline_from_config, load_data, eval_model


# load_dotenv()

def train_and_log_model():
    config = load_config(MODEL_CONFIG_PATH)

    configure_mlflow()

    X_train, X_test, y_train, y_test = load_data(include_feedback=False)
    pipeline = create_pipeline_from_config(config)

    with mlflow.start_run() as run:
        pipeline.fit(X_train, y_train)
        rmse = eval_model(pipeline, X_test, y_test)

        def log_params(prefix, d):
            for k, v in d.items():
                if isinstance(v, dict):
                    log_params(f"{prefix}.{k}", v)
                else:
                    mlflow.log_param(f"{prefix}.{k}", v)

        log_params("", config)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_artifact(MODEL_CONFIG_PATH, artifact_path="config")
        log_model(pipeline)
        register_model(run.info.run_id, alias="production")

if __name__ == "__main__":
    train_and_log_model()
