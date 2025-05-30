import logging
import sys

from api.routes import router
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()


def setup_logging():
    """Configure the root logger with console output and proper formatting."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)


setup_logging()

# Get logger for this module
logger = logging.getLogger(__name__)

app = FastAPI(title="MLServe API", version="1.0")

app.include_router(router)


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "API running 🚀"}
