"""Plugin execution endpoints."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from wtf_api.models import (
    PluginExecutionRequest,
    PluginExecutionResponse,
    ExecutionStatus
)
from wtf_api.services.execution_service import (
    execute_plugins,
    get_execution_status,
    list_executions
)

router = APIRouter()


@router.post("/execute", response_model=PluginExecutionResponse)
async def execute_plugins_sync(request: PluginExecutionRequest):
    """
    Execute plugins synchronously.
    
    Runs the requested plugins and waits for completion.
    Returns results when all plugins have finished.
    """
    try:
        result = execute_plugins(
            timeout=request.timeout,
            max_concurrent=request.max_concurrent,
            plugin_args=request.plugin_args,
            output_dir=request.output_dir
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute/async")
async def execute_plugins_async(
    request: PluginExecutionRequest,
    background_tasks: BackgroundTasks
):
    """
    Execute plugins asynchronously.
    
    Starts plugin execution in the background and returns immediately
    with an execution ID. Use GET /execution/{id} to check status.
    """
    # TODO: Implement async execution with task tracking
    return {
        "execution_id": "placeholder",
        "status": "queued",
        "message": "Async execution not yet implemented"
    }


@router.get("/execution/{execution_id}", response_model=ExecutionStatus)
async def get_execution(execution_id: str):
    """
    Get status of an async execution.
    
    Args:
        execution_id: ID returned from async execution request
    """
    status = get_execution_status(execution_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return status


@router.get("/executions", response_model=list[ExecutionStatus])
async def list_all_executions():
    """
    List all executions (recent history).
    
    Returns status of recent plugin executions.
    """
    return list_executions()


@router.delete("/execution/{execution_id}")
async def cancel_execution(execution_id: str):
    """
    Cancel a running execution.
    
    Args:
        execution_id: ID of execution to cancel
    """
    # TODO: Implement execution cancellation
    return {
        "execution_id": execution_id,
        "status": "cancelled",
        "message": "Cancellation not yet implemented"
    }
