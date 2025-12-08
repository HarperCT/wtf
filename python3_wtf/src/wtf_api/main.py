"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from wtf_api.routers import plugins, execution, health

app = FastAPI(
    title="WheresTheFault API",
    description="API for collecting system debugging information",
    version="0.1.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(plugins.router, prefix="/api/v1", tags=["plugins"])
app.include_router(execution.router, prefix="/api/v1", tags=["execution"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "WheresTheFault API",
        "version": "0.1.0",
        "docs": "/docs"
    }
