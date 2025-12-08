#!/usr/bin/env python3
"""Development server runner."""
import uvicorn
from wtf_api.config import settings


def run_dev_server():
    """Run development server with auto-reload."""
    uvicorn.run(
        "wtf_api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )


def run_prod_server():
    """Run production server."""
    uvicorn.run(
        "wtf_api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=4,
        log_level="warning"
    )


if __name__ == "__main__":
    run_dev_server()
