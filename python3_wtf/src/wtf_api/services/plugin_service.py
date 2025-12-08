"""Service for plugin discovery and management."""
from pathlib import Path
from python3_wtf.plugin_manager import import_plugins, PLUGIN_DIR
from python3_wtf.plugins.plugin import Plugin
from wtf_api.models import PluginInfo


def get_available_plugins() -> list[type[Plugin]]:
    """
    Get all available plugin classes.
    
    Returns:
        List of plugin classes
    """
    plugins = import_plugins(
        PLUGIN_DIR,
        base_class=Plugin,
        create_instance=False,
        filter_abstract=True
    )
    return plugins


def check_plugin_applicable(plugin_class: type[Plugin]) -> bool:
    """
    Check if a plugin is applicable on this system.
    
    Args:
        plugin_class: Plugin class to check
        
    Returns:
        True if plugin can run on this system
    """
    try:
        instance = plugin_class()
        return instance.is_applicable()
    except Exception:
        return False


def get_plugin_info(plugin_name: str) -> PluginInfo | None:
    """
    Get information about a specific plugin.
    
    Args:
        plugin_name: Name of plugin (case-insensitive)
        
    Returns:
        PluginInfo or None if not found
    """
    plugins = get_available_plugins()
    
    for plugin_class in plugins:
        if plugin_class.__name__.lower() == plugin_name.lower():
            try:
                instance = plugin_class()
                return PluginInfo(
                    name=plugin_class.__name__,
                    is_applicable=instance.is_applicable(),
                    is_configurable=instance.is_configurable,
                    is_multirunable=instance.is_multirunable
                )
            except Exception:
                return None
    
    return None


def get_plugin_class(plugin_name: str) -> type[Plugin] | None:
    """
    Get plugin class by name.
    
    Args:
        plugin_name: Name of plugin (case-insensitive)
        
    Returns:
        Plugin class or None if not found
    """
    plugins = get_available_plugins()
    
    for plugin_class in plugins:
        if plugin_class.__name__.lower() == plugin_name.lower():
            return plugin_class
    
    return None
