import tempfile
import os
import shutil
import sys

import pytest
from plugins.plugin import Plugin
import plugin_manager
from common_test_functions import PluginStub, BadPluginStub, UnapplicablePluginStub

class TestPluginFinder:
    def test_fetch_plugins(self):
        def mock_import_plugins(plugins_package_directory_path=None, base_class=None, create_instance=True, filter_abstract=True):
            return [PluginStub, BadPluginStub, UnapplicablePluginStub]
        mock_import = pytest.MonkeyPatch()
        mock_import.setattr(plugin_manager, "import_plugins", mock_import_plugins)
        x = plugin_manager.PluginManager()
        assert x.plugins_detected == [PluginStub, BadPluginStub, UnapplicablePluginStub]

    def test_applicable_plugins(self):
        def mock_import_plugins(plugins_package_directory_path=None, base_class=None, create_instance=True, filter_abstract=True):
            return [PluginStub, BadPluginStub, UnapplicablePluginStub]
        mock_import = pytest.MonkeyPatch()
        mock_import.setattr(plugin_manager, "import_plugins", mock_import_plugins)
        x = plugin_manager.PluginManager()
        for plugin in x.applicable_plugins:
            assert isinstance(plugin, (PluginStub, BadPluginStub))

    def test_no_applicable_plugins(self):
        def mock_import_plugins(plugins_package_directory_path=None, base_class=None, create_instance=True, filter_abstract=True):
            return []
        mock_import = pytest.MonkeyPatch()
        mock_import.setattr(plugin_manager, "import_plugins", mock_import_plugins)
        x = plugin_manager.PluginManager()
        assert x.applicable_plugins == []


@pytest.mark.skip("Harper will come back to this and figure it out eventually")
def test_import_plugins():
    with tempfile.TemporaryDirectory() as temp_dir:
        # setup temp_dir
        temp_plugin_path = os.path.join(temp_dir, "test_plugin.py")
        temp_file_path = os.path.join(temp_dir, "__init__.py")
        with open(temp_file_path, "w") as f:
            f.write("")
        shutil.copy2("python3-wtf/test/common_test_functions.py", temp_plugin_path)
        # print("BANG")
        # print(os.listdir(temp_dir))
        # sys.path.append(temp_file_path)
        # do test
        plugins = plugin_manager.import_plugins(temp_dir, Plugin, True)
        print(plugins)