from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

# Include API Routers
app.include_router(health_router, prefix="/api/v1")
