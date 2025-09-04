
import unittest
from unittest import mock

from python3_wtf.plugins.plugin import Plugin
from python3_wtf.plugin_manager import PluginManager


class DummyPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.is_multirunable = False
        self.is_configurable = False
        self._applied = False

    def is_applicable(self) -> bool:
        return True

    def run(self) -> str:
        return "dummy run fn"

    def configure_args(self, plugin_args: tuple) -> None:
        self._applied = True


class ConfigurablePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.is_configurable = True
        self.is_multirunable = False

    def is_applicable(self) -> bool:
        return True

    def run(self) -> str:
        return "configurable run fn"

    def configure_args(self, plugin_args: tuple) -> None:
        self.command = plugin_args


class NonConfigurablePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.is_configurable = False
        self.is_multirunable = True

    def is_applicable(self) -> bool:
        return True

    def run(self) -> str:
        return "non configurable run fn"


class NotApplicablePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.is_configurable = True
        self.is_multirunable = True

    def is_applicable(self) -> bool:
        return False

    def run(self) -> str:
        return "not applicable run fn"


class FakePlugin:
    def __init__(self):
        pass


class TestPluginManager(unittest.TestCase):

    @mock.patch("python3_wtf.plugin_manager.import_plugins", return_value=[DummyPlugin])
    def test_manager_initialization_no_args(self, mock_import):
        manager = PluginManager(plugins_args=[])
        self.assertEqual(len(manager.plugins_detected), 1)
        self.assertEqual(len(manager.applicable_plugins), 1)
        self.assertIsInstance(manager.applicable_plugins[0], DummyPlugin)

    @mock.patch("python3_wtf.plugin_manager.import_plugins", return_value=[DummyPlugin])
    def test_manager_with_args(self, mock_import):
        manager = PluginManager(plugins_args=[("DummyPlugin", "arg1")])
        self.assertEqual(len(manager.applicable_plugins), 1)
        plugin_instance = manager.applicable_plugins[0]
        self.assertTrue(plugin_instance.is_applicable())
        self.assertFalse(plugin_instance._applied)

    @mock.patch("python3_wtf.plugin_manager.import_plugins", return_value=[])
    def test_manager_no_plugins_found(self, mock_import):
        manager = PluginManager(plugins_args=[])
        self.assertEqual(len(manager.plugins_detected), 0)
        self.assertEqual(len(manager.applicable_plugins), 0)

    @mock.patch(
        "python3_wtf.plugin_manager.import_plugins",
        return_value=[ConfigurablePlugin]
    )
    def test_configurable_plugin_skipped_without_args(self, mock_import):
        with self.assertLogs("python3_wtf.plugin_manager", level="INFO") as cm:
            manager = PluginManager(plugins_args=[])
        self.assertEqual(len(manager.applicable_plugins), 0)
        log_output = "\n".join(cm.output)
        self.assertIn("Not adding ConfigurablePlugin", log_output)

    @mock.patch(
        "python3_wtf.plugin_manager.import_plugins",
        return_value=[
            ConfigurablePlugin,
            NonConfigurablePlugin,
            NotApplicablePlugin
        ])
    def test_full_branches(self, mock_import):
        plugin_args = [
            ("ConfigurablePlugin", "arg1", "arg2"),  # normal configurable
            ("NonConfigurablePlugin", "arg1"),       # non-configurable receiving args
            ("NotFoundPlugin", "arg"),               # no matching class
            ("NotApplicablePlugin", "arg1"),         # matched but not applicable
        ]

        with self.assertLogs("python3_wtf.plugin_manager", level="INFO") as cm:
            manager = PluginManager(plugins_args=plugin_args)

        # Configurable plugin should be instantiated and configured
        configurable_instance = next(
            (
                p for p in manager.applicable_plugins
                if isinstance(p, ConfigurablePlugin)
            ),
            None
        )
        self.assertIsNotNone(configurable_instance)
        self.assertEqual(configurable_instance.command, ["arg1", "arg2"])

        # Non-configurable plugin should still be instantiated but log a warning
        self.assertTrue(any(
            "'NonConfigurablePlugin' not configurable" in m for m in cm.output
        ))

        # Plugin not found should log a warning
        self.assertTrue(any("No plugin instance found matching 'notfoundplugin'" in m
                            for m in cm.output))

        # Not applicable plugin should be skipped
        self.assertFalse(any(
            isinstance(p, NotApplicablePlugin) for p in manager.applicable_plugins
        ))

    def test_if_plugin_isnt_a_plugin(self):
        manager = PluginManager.__new__(PluginManager)  # bypass __init__
        manager.plugins_detected = [FakePlugin]
        manager.applicable_plugins = []
        manager.plugins_args = [("FakePlugin", "arg1")]

        with self.assertLogs("python3_wtf.plugin_manager", level="DEBUG") as cm:
            manager.instantiate_plugins_from_args()
        self.assertTrue(any("I'll be shocked" in m for m in cm.output))

    @mock.patch(
        "python3_wtf.plugin_manager.import_plugins",
        return_value=[ConfigurablePlugin, ConfigurablePlugin]
    )
    def test_non_multirunnable_duplicate_warning(self, mock_import):
        plugin_args = [
            ("ConfigurablePlugin", "arg1"),
            ("ConfigurablePlugin", "arg2")
        ]

        with self.assertLogs("python3_wtf.plugin_manager", level="WARNING") as cm:
            manager = PluginManager(plugins_args=plugin_args)

        self.assertTrue(any(
            "is not multi-runnable and already instantiated" in m
            for m in cm.output
        ))

        instances = [
            p for p in manager.applicable_plugins if isinstance(
                p, ConfigurablePlugin
            )
        ]
        self.assertEqual(len(instances), 1)
