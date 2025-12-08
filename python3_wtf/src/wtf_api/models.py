"""Pydantic models for API request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional


class PluginInfo(BaseModel):
    """Information about a plugin."""
    name: str
    is_applicable: bool
    is_configurable: bool
    is_multirunable: bool


class PluginExecutionRequest(BaseModel):
    """Request to execute plugins."""
    timeout: int = Field(default=5, ge=1, description="Timeout in seconds")
    max_concurrent: Optional[int] = Field(default=None, ge=0, description="Max concurrent plugins")
    plugin_args: list[dict[str, list[str]]] = Field(default=[], description="Plugin configurations")
    output_dir: Optional[str] = Field(default=None, description="Output directory path")


class PluginExecutionResponse(BaseModel):
    """Response from plugin execution."""
    status: str
    message: str
    archive_path: Optional[str] = None
    plugins_run: int
    plugins_succeeded: int
    plugins_failed: int


class PluginResult(BaseModel):
    """Result from a single plugin execution."""
    plugin_name: str
    stdout: str
    stderr: str
    timed_out: bool
    success: bool


class ExecutionStatus(BaseModel):
    """Status of an ongoing execution."""
    execution_id: str
    status: str  # "running", "completed", "failed"
    progress: float  # 0.0 to 1.0
    plugins_completed: int
    plugins_total: int
    started_at: str
    completed_at: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    plugins_available: int
