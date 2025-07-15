from fastapi import FastAPI

from src.db.engine import engine
from src.integration import setup_integration
from src.task.api.rest import router as task_router
import src.core.logging_setup
from src.core.logging_setup import setup_fastapi_logging

app = FastAPI(title="Sora API")
setup_fastapi_logging(app)
setup_integration(app)

app.include_router(task_router, tags=["Task"], prefix="/api/task")


