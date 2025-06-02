from db.client import Base, engine
from db.models import PredictionLog


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
