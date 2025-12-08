"""Health check endpoints."""
from fastapi import APIRouter
from wtf_api.models import HealthResponse
from wtf_api.services.plugin_service import get_available_plugins

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns API status and basic information.
    """
    plugins = get_available_plugins()
    
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        plugins_available=len(plugins)
    )


@router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"status": "ok"}
