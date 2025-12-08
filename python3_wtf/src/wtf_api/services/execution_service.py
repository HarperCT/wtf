"""Service for executing plugins."""
from pathlib import Path
from python3_wtf.main import WheresTheFault
from wtf_api.models import PluginExecutionResponse, ExecutionStatus


# TODO: Implement proper execution tracking
_executions = {}


def execute_plugins(
    timeout: int,
    max_concurrent: int | None,
    plugin_args: list[dict[str, list[str]]],
    output_dir: str | None
) -> PluginExecutionResponse:
    """
    Execute plugins synchronously.
    
    Args:
        timeout: Timeout in seconds
        max_concurrent: Max concurrent plugins
        plugin_args: Plugin configurations
        output_dir: Output directory path
        
    Returns:
        Execution response with results
    """
    # Convert plugin_args from API format to internal format
    # API: [{"plugin_name": ["arg1", "arg2"]}]
    # Internal: [("plugin_name", "arg1", "arg2")]
    internal_plugin_args = []
    for plugin_dict in plugin_args:
        for name, args in plugin_dict.items():
            internal_plugin_args.append((name, *args))
    
    # Set default output directory
    if not output_dir:
        output_dir = "/tmp"
    
    try:
        # Execute using WheresTheFault
        wtf = WheresTheFault(
            timeout=timeout,
            output_dir=Path(output_dir),
            plugin_args=internal_plugin_args,
            max_concurrent=max_concurrent
        )
        
        # TODO: Capture results properly
        wtf.main_runner()
        
        # TODO: Get actual results from execution
        return PluginExecutionResponse(
            status="success",
            message="Plugins executed successfully",
            archive_path=str(output_dir),
            plugins_run=len(internal_plugin_args) or 0,
            plugins_succeeded=len(internal_plugin_args) or 0,
            plugins_failed=0
        )
        
    except Exception as e:
        return PluginExecutionResponse(
            status="error",
            message=str(e),
            archive_path=None,
            plugins_run=0,
            plugins_succeeded=0,
            plugins_failed=0
        )


def get_execution_status(execution_id: str) -> ExecutionStatus | None:
    """
    Get status of an execution.
    
    Args:
        execution_id: Execution ID
        
    Returns:
        ExecutionStatus or None if not found
    """
    # TODO: Implement execution tracking
    return _executions.get(execution_id)


def list_executions() -> list[ExecutionStatus]:
    """
    List all recent executions.
    
    Returns:
        List of execution statuses
    """
    # TODO: Implement execution history
    return list(_executions.values())
