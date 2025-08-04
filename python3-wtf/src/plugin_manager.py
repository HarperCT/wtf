import os
import importlib
import glob
import logging

from pathlib import Path
from plugins.plugin import Plugin
from inspect import isabstract, isclass


logger = logging.getLogger(__name__)

# WARNING: this expects a directory called plugins to live under it, moving it will cause no plugins to be detected... careful on changing project scructure
TOP_DIR = Path(os.path.dirname(__file__))
PLUGIN_DIR = TOP_DIR / Path("plugins")

class PluginManager:
    plugins_detected: list[Plugin]
    applicable_plugins: list[Plugin]

    def __init__(self, plugins_args):
        self.plugins_detected = []
        self.applicable_plugins = []
        self.plugins_args = plugins_args
        self.fetch_plugins()
        self.instantiate_plugins_with_no_args()
        if self.plugins_args:
            self.instantiate_plugins_from_args()
    
    def fetch_plugins(self):
        self.plugins_detected = import_plugins(PLUGIN_DIR, base_class=Plugin, create_instance=False)
        logger.info(f"Found plugins {self.plugins_detected}")

    def instantiate_plugins_with_no_args(self):
        # Instantiate zero-arg, non-configurable, non-multirunable plugins
        for plugin_cls in self.plugins_detected:
            instance = plugin_cls()
            if instance.is_applicable():
                # Add default instance only if it's not already present
                if not instance.is_configurable and not instance.is_multirunable:
                    self.applicable_plugins.append(instance)
                    logger.info(f"Added non-configurable plugin: {instance.__class__.__name__}")
                elif instance.is_configurable and not self.plugins_args:
                    logger.info(f"Not adding {instance.__class__.__name__} as it needs to be configured with plugin_args. Consider adding some to get this plugin")

    def instantiate_plugins_from_args(self):
        for plugin_args in self.plugins_args:
            plugin_name = plugin_args[0].lower()
            plugin_params = plugin_args[1:]

            # Find plugin class whose name contains plugin_name (case-insensitive)
            matched_class = None
            for plugin_cls in self.plugins_detected:
                cls_name = plugin_cls.__name__.lower()
                if plugin_name in cls_name:
                    matched_class = plugin_cls
                    break

            if matched_class is None:
                logger.warning(f"No plugin instance found matching '{plugin_name}', skipping.")
                continue

            plugin_instance = matched_class()

            if not plugin_instance.is_applicable():
                logger.info(f"Plugin '{plugin_instance.__class__.__name__}' not applicable, skipping.")
                continue

            if not plugin_instance.is_configurable:
                logger.warning(f"Plugin '{plugin_instance.__class__.__name__}' not configurable, you should remove it from your plugin_args, skipping.")
                continue

            if not plugin_instance.is_multirunable:
                already_exists = any(
                    isinstance(existing, plugin_instance)
                    for existing in self.applicable_plugins
                )
                if already_exists:
                    logger.info(f"Plugin '{plugin_name}' is not multi-runnable and already instantiated. Skipping duplicate.")
                    continue

            if plugin_instance.is_configurable:
                plugin_instance.configure_args([*plugin_params])
            else:
                if plugin_params:
                    logger.warning(f"Plugin '{plugin_name}' is not configurable but received args. Ignoring args.")

            self.applicable_plugins.append(plugin_instance)
            logger.info(f"Instantiated plugin: {plugin_instance.__class__.__name__} with args: {plugin_params}")

def import_plugins(plugins_package_directory_path, base_class=None, create_instance=True, filter_abstract=True):

    plugins_package_name = os.path.basename(plugins_package_directory_path)
    return_values: list[Plugin] = []

    # -----------------------------
    # Iterate all python files within that directory
    plugin_file_paths = glob.glob(os.path.join(plugins_package_directory_path, "*.py"))
    for plugin_file_path in plugin_file_paths:
        plugin_file_name = os.path.basename(plugin_file_path)

        module_name = os.path.splitext(plugin_file_name)[0]

        if module_name.startswith("__"):
            logger.debug(f"Found module but not processing associated plugins: {module_name}")
            continue

        # -----------------------------
        # Import python file

        module = importlib.import_module("." + module_name, package=plugins_package_name)

        # -----------------------------
        # Iterate items inside imported python file

        for item in dir(module):
            value = getattr(module, item)
            if not value:
                logger.debug(f"Found nothing: {value}")
                continue

            if not isclass(value):
                logger.debug(f"Found non-class plugin: {value}")
                continue
            if filter_abstract and isabstract(value):
                logger.debug(f"Found abstract plugin: {value}")
                continue
            
            if base_class is not None:
                if type(value) != type(base_class):
                    continue

            # -----------------------------
            # Instantiate / return type (depends on create_instance)
            return_values.append(value() if create_instance else value)
    return return_values
