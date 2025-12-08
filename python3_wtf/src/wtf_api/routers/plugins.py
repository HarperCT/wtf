"""Plugin discovery and information endpoints."""
from fastapi import APIRouter, HTTPException
from wtf_api.models import PluginInfo
from wtf_api.services.plugin_service import (
    get_available_plugins,
    get_plugin_info,
    check_plugin_applicable
)

router = APIRouter()


@router.get("/plugins", response_model=list[PluginInfo])
async def list_plugins():
    """
    List all available plugins.
    
    Returns information about all discovered plugins including
    their applicability on the current system.
    """
    plugins = get_available_plugins()
    return [
        PluginInfo(
            name=plugin.__name__,
            is_applicable=check_plugin_applicable(plugin),
            is_configurable=getattr(plugin(), 'is_configurable', False),
            is_multirunable=getattr(plugin(), 'is_multirunable', False)
        )
        for plugin in plugins
    ]


@router.get("/plugins/{plugin_name}", response_model=PluginInfo)
async def get_plugin(plugin_name: str):
    """
    Get information about a specific plugin.
    
    Args:
        plugin_name: Name of the plugin (case-insensitive)
    """
    plugin_info = get_plugin_info(plugin_name)
    
    if not plugin_info:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    
    return plugin_info


@router.get("/plugins/{plugin_name}/applicable")
async def check_plugin(plugin_name: str):
    """
    Check if a plugin is applicable on this system.
    
    Args:
        plugin_name: Name of the plugin
    """
    plugin_info = get_plugin_info(plugin_name)
    
    if not plugin_info:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    
    return {
        "plugin_name": plugin_name,
        "is_applicable": plugin_info.is_applicable
    }
