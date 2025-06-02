import tempfile
from datetime import datetime

import yaml
import mlflow
from mlflow.tracking import MlflowClient

from utils.settings import MLFLOW_TRACKING_URI, MODEL_NAME, MODEL_ALIAS

client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)



def log_model(model):
    mlflow.sklearn.log_model(model, artifact_path="model")


def register_model(run_id: str, alias: str | None = None):
    model_uri = f"runs:/{run_id}/model"
    registered_model = mlflow.register_model(model_uri, MODEL_NAME)

    if alias:
        client.set_registered_model_alias(
            name=MODEL_NAME,
            alias=alias,
            version=registered_model.version,
        )

def load_latest_model():
    model_uri = f"models:/{MODEL_NAME}@production"
    model = mlflow.sklearn.load_model(model_uri)
    return model


def load_latest_model_info():

    model_version = client.get_model_version_by_alias(MODEL_NAME, "production")
    model_details = client.get_model_version(
        name=MODEL_NAME, version=model_version.version
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = client.download_artifacts(
            model_version.run_id, "config/model_config.yaml", tmpdir
        )
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    return {
        "name": MODEL_NAME,
        "version": model_version.version,
        "run_id": model_version.run_id,
        "creation_time": datetime.fromtimestamp(
            model_details.creation_timestamp / 1000
        ).isoformat(),
        "config": config,
    }



# def log_model(model, register_alias: str | None = None):
#     mlflow.sklearn.log_model(
#         model, artifact_path="model", registered_model_name=MODEL_NAME
#     )

#     if register_alias:
#         latest_versions = client.get_latest_versions(MODEL_NAME)
#         latest_version = max(int(v.version) for v in latest_versions)
#         client.set_registered_model_alias(
#             MODEL_NAME, register_alias, str(latest_version)
#         )



