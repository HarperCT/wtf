import os
import importlib
import logging

from pathlib import Path
from python3_wtf.plugins.plugin import Plugin
from inspect import isabstract, isclass, getmembers


logger = logging.getLogger(__name__)

# WARNING: this expects a directory called plugins
# to live under it, moving it will cause no plugins
# to be detected... careful on changing project scructure
TOP_DIR = Path(os.path.dirname(__file__))
PLUGIN_DIR = TOP_DIR / Path("plugins")
BASE_DIR = Path("python3-wtf")


class PluginManager:
    plugins_detected: list[Plugin]
    applicable_plugins: list[Plugin]
    plugins_args: list[tuple[str, ...]]
    _plugin_lookup: dict[str, type[Plugin]]  # Cache for fast name lookup

    def __init__(self, plugins_args: list[tuple[str, ...]]):
        self.plugins_detected = []
        self.applicable_plugins = []
        self.plugins_args = plugins_args
        self._plugin_lookup = {}
        self.fetch_plugins()
        self.instantiate_plugins_with_no_args()
        if self.plugins_args:
            self.instantiate_plugins_from_args()

    def fetch_plugins(self):
        self.plugins_detected = import_plugins(PLUGIN_DIR,
                                               base_class=Plugin,
                                               create_instance=False)
        # Build lookup dict for O(1) plugin name matching
        self._plugin_lookup = {
            cls.__name__.lower(): cls for cls in self.plugins_detected
        }
        logger.info(f"Found {len(self.plugins_detected)} plugins: "
                   f"{[cls.__name__ for cls in self.plugins_detected]}")

    def instantiate_plugins_with_no_args(self):
        # Instantiate zero-arg, non-configurable, non-multirunable plugins
        for plugin_cls in self.plugins_detected:
            # Create temporary instance to check flags (cheap operation)
            temp_instance = plugin_cls()
            
            # Skip if configurable or multirunable - these need explicit args
            if temp_instance.is_configurable or temp_instance.is_multirunable:
                if temp_instance.is_configurable and not self.plugins_args:
                    logger.info(
                        f"Not adding {plugin_cls.__name__} "
                        "as it needs to be configured with "
                        "plugin_args. Consider adding some "
                        "to get this plugin."
                    )
                continue
            
            # Only check is_applicable for plugins we'll actually use
            if temp_instance.is_applicable():
                self.applicable_plugins.append(temp_instance)
                logger.info(f"Added non-configurable plugin: {plugin_cls.__name__}")

    def instantiate_plugins_from_args(self):
        for plugin_args in self.plugins_args:
            plugin_name = plugin_args[0].lower()
            plugin_params = plugin_args[1:]

            # Fast O(1) lookup using dict - try exact match first
            matched_class = self._plugin_lookup.get(plugin_name)
            
            # Fall back to substring match if exact match fails
            if matched_class is None:
                for cls_name, plugin_cls in self._plugin_lookup.items():
                    if plugin_name in cls_name:
                        matched_class = plugin_cls
                        break

            if matched_class is None:
                logger.warning(
                    f"No plugin found matching '{plugin_name}'. "
                    f"Available: {list(self._plugin_lookup.keys())}"
                )
                continue

            plugin_instance: Plugin = matched_class()

            if not isinstance(plugin_instance, Plugin):
                logger.debug(
                    "I'll be shocked if we ever hit this, "
                    "but typing is having a hissy... "
                    "if we do report me!"
                )
                continue

            if not plugin_instance.is_applicable():
                logger.warning(
                    f"Plugin '{plugin_instance.__class__.__name__}'"
                    "not applicable, skipping."
                )
                continue

            if not plugin_instance.is_configurable:
                logger.warning(
                    f"Plugin '{plugin_instance.__class__.__name__}' "
                    "not configurable, you should remove it "
                    "from your plugin_args, skipping."
                )
                continue

            if not plugin_instance.is_multirunable:
                already_exists = any(
                    isinstance(existing, type(plugin_instance))
                    for existing in self.applicable_plugins
                )
                if already_exists:
                    logger.warning(
                        f"Plugin '{plugin_name}' is not "
                        "multi-runnable and already "
                        "instantiated. Skipping duplicate."
                    )
                    continue

            if plugin_instance.is_configurable:
                plugin_instance.configure_args([*plugin_params])
            else:
                if plugin_params:
                    logger.warning(
                        f"Plugin '{plugin_name}' is not "
                        "configurable but received args."
                        "Ignoring args."
                    )

            self.applicable_plugins.append(plugin_instance)
            logger.info(f"Instantiated plugin: \
                        {plugin_instance.__class__.__name__} \
                        with args: {plugin_params}")


def import_plugins(
    plugins_package_directory_path,
    base_class=None,
    create_instance=True,
    filter_abstract=True
):
    """
    Discovers and imports plugin classes from a directory.
    Optimized to reduce unnecessary imports and iterations.
    """
    plugins_package_name = (
        f"python3_wtf.{os.path.basename(plugins_package_directory_path)}"
    )
    return_values: list[Plugin] = []
    
    # Use pathlib for cleaner path handling
    plugin_dir = Path(plugins_package_directory_path)
    
    # Iterate all python files within that directory
    for plugin_file_path in plugin_dir.glob("*.py"):
        module_name = plugin_file_path.stem
        
        # Skip __init__ and other dunder files
        if module_name.startswith("__"):
            logger.debug(f"Skipping module: {module_name}")
            continue

        try:
            # Import python file
            module = importlib.import_module(
                f".{module_name}",
                package=plugins_package_name
            )
            
            # Use getmembers with predicate for efficient filtering
            # This is faster than dir() + getattr() + multiple checks
            def is_plugin_class(obj):
                return (
                    isclass(obj) and
                    obj is not base_class and  # Don't include base class itself
                    (not filter_abstract or not isabstract(obj)) and
                    (base_class is None or issubclass(obj, base_class)) and
                    obj.__module__ == module.__name__  # Only classes defined in this module
                )
            
            plugin_classes = getmembers(module, is_plugin_class)
            
            for name, plugin_cls in plugin_classes:
                # Instantiate or return class depending on flag
                return_values.append(plugin_cls() if create_instance else plugin_cls)
                logger.debug(f"Loaded plugin: {name}")
                
        except Exception as e:
            logger.error(f"Failed to import plugin from {module_name}: {e}")
            continue
    
    return return_values
