from db.client import Base
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, Text, func


class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    __table_args__ = {"schema": "predictions"}

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    model_name = Column(Text, nullable=False)
    model_version = Column(Text)
    mlflow_run_id = Column(Text)
    prediction = Column(Float, nullable=False)
    input_data = Column(JSON, nullable=False)
    user_notes = Column(Text)
    extra_metadata = Column(JSON)


class PredictionFeedback(Base):
    __tablename__ = "prediction_feedback"
    __table_args__ = {"schema": "predictions"}

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    prediction_id = Column(Integer, ForeignKey("predictions.prediction_logs.id"))
    feedback = Column(Float, nullable=False)
    retraining_run_id = Column(Text, nullable=True)