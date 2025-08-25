import unittest
from unittest.mock import patch
from pathlib import Path
from python3_wtf.main import WheresTheFault


class TestWheresTheFaultMain(unittest.TestCase):
    def setUp(self):
        self.sample_args = [
            ("plugin1", "arg1"),
            ("plugin2", "arg2")
        ]
        self.output_dir = Path("/tmp")

    @patch("python3_wtf.main.archive_outputs")
    @patch("python3_wtf.main.ThreadRunner")
    @patch("python3_wtf.main.PluginManager")
    def test_main_runner_success(
        self,
        MockPluginManager,
        MockThreadRunner,
        mock_archive
    ):
        """Test that main_runner runs plugins and archives outputs."""

        fake_plugins = ["p1", "p2"]
        fake_outputs = {"p1": "result1", "p2": "result2"}

        mock_plugin_manager = MockPluginManager.return_value
        mock_plugin_manager.applicable_plugins = fake_plugins

        mock_runner = MockThreadRunner.return_value
        mock_runner.run_threads.return_value = fake_outputs

        wtf = WheresTheFault(
            timeout=5,
            output_dir=self.output_dir,
            plugin_args=self.sample_args
        )
        wtf.main_runner()

        MockPluginManager.assert_called_once_with(self.sample_args)
        MockThreadRunner.assert_called_once_with(timeout=5, plugins=fake_plugins)
        mock_runner.run_threads.assert_called_once()
        mock_archive.assert_called_once_with(fake_outputs, "/tmp")

    @patch("python3_wtf.main.ThreadRunner")
    @patch("python3_wtf.main.PluginManager")
    def test_main_runner_no_plugins(self, MockPluginManager, MockThreadRunner):
        """Test behavior when no plugins are applicable."""

        mock_plugin_manager = MockPluginManager.return_value
        mock_plugin_manager.applicable_plugins = []

        wtf = WheresTheFault(
            timeout=5,
            output_dir=self.output_dir,
            plugin_args=self.sample_args
        )

        # The code creates an Exception but doesn't raise it
        with self.assertRaises(Exception):
            wtf.main_runner()

        # ThreadRunner should never be called
        MockThreadRunner.assert_not_called()
