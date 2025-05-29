CREATE SCHEMA IF NOT EXISTS mlflow;
CREATE SCHEMA IF NOT EXISTS predictions;

CREATE TABLE IF NOT EXISTS predictions.prediction_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    input_data JSONB NOT NULL,
    prediction_result JSONB NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT,
    mlflow_run_id TEXT,
    user_notes TEXT,
    extra_metadata JSONB
);
