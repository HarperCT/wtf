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

class PluginDetector:
    plugins_detected: list[Plugin]
    applicable_plugins: list[Plugin]

    def __init__(self):
        self.plugins_detected = []
        self.applicable_plugins = []
        self.fetch_plugins()
    
    def fetch_plugins(self):
        self.plugins_detected = import_plugins(PLUGIN_DIR, base_class=Plugin, create_instance=False)
        logger.info(f"Found plugins {self.plugins_detected}")
        self.get_applicable_plugins()
        
    def get_applicable_plugins(self):
        if self.plugins_detected:
            self.applicable_plugins = []
            for plugin in self.plugins_detected:
                if plugin().is_applicable():
                    self.applicable_plugins.append(plugin)
            logger.info(f"Applicable plugins: {self.applicable_plugins}")


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

PluginDetector()