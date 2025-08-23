import json
import os
import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from pathlib import Path
from python3_wtf.wtf_cli import cli

TEST_SETTINGS_FILE = {
    "timeout": 5,
    "output_dir": "/tmp",
    "plugins": [
        {"tshark": ["-i", "lo"]},
        {"tshark": ["-i", "enp0s3"]}
    ]
}

class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        patcher = patch("python3_wtf.wtf_cli.WheresTheFault")
        self.mock_class = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_instance = self.mock_class.return_value

    def test_cli_required_options(self):
        with self.runner.isolated_filesystem():
            tmp_dir = Path("output")
            tmp_dir.mkdir()
            result = self.runner.invoke(cli, ['-t', '3', '-o', str(tmp_dir)])
            assert result.exit_code == 0
            assert "[WheresTheFault] Initializing WheresTheFault..." in result.output
            assert f"[WheresTheFault] Running with timeout=3, output_dir='{tmp_dir.resolve()}' and plugin_args=None" in result.output
            assert "[WheresTheFault] Done." in result.output
            assert self.mock_instance.main_runner.called

    def test_cli_missing_timeout(self):
        with self.runner.isolated_filesystem():
            tmp_dir = Path("output")
            tmp_dir.mkdir()
            result = self.runner.invoke(cli, ['-o', str(tmp_dir)])
            assert result.exit_code != 0
            assert "Missing required parameters: 'timeout' and/or 'output_dir' must be set either in the CLI or .json.\n" in result.output
            assert not self.mock_instance.main_runner.called

    def test_cli_invalid_timeout(self):
        with self.runner.isolated_filesystem():
            tmp_dir = Path("output")
            tmp_dir.mkdir()
            result = self.runner.invoke(cli, ['-t', '0', '-o', str(tmp_dir)])
            assert result.exit_code != 0
            assert "Invalid value for '-t' / '--timeout'" in result.output
            assert not self.mock_instance.main_runner.called

    def test_cli_invalid_output_dir(self):
        result = self.runner.invoke(cli, ['-t', '5', '-o', '/non/existing/path'])
        assert result.exit_code != 0
        assert "Invalid value for '-o' / '--output-dir'" in result.output
        assert not self.mock_instance.main_runner.called

    def test_plugin_with_list_args(self):
        with self.runner.isolated_filesystem():
            Path("output").mkdir()
            result = self.runner.invoke(cli, [
                '-t', '5', '-o', 'output',
                '-p', 'example_plugin', '["arg1", "arg2"]'
            ])
            assert result.exit_code == 0
            assert "plugin_args=[('example_plugin', 'arg1', 'arg2')]" in result.output
            assert self.mock_instance.main_runner.called

    def test_multiple_plugins_mixed_args(self):
        with self.runner.isolated_filesystem():
            Path("output").mkdir()
            result = self.runner.invoke(cli, [
                '-t', '5', '-o', 'output',
                '-p', 'pluginA', '["x", "y"]',
                '-p', 'pluginB', '["one", "two", "three"]'
            ])
            assert result.exit_code == 0
            assert "plugin_args=[('pluginA', 'x', 'y'), ('pluginB', 'one', 'two', 'three')]" in result.output
            assert self.mock_instance.main_runner.called

    def test_plugin_with_bad_format_raises(self):
        with self.runner.isolated_filesystem():
            Path("output").mkdir()
            result = self.runner.invoke(cli, [
                '-t', '3', '-o', 'output',
                '-p', 'bad_plugin', '"{not: a list}"'
            ])
            assert result.exit_code != 0
            assert 'Invalid value: Plugin args must be a valid list or a space-separated string' in result.output
            assert not self.mock_instance.main_runner.called

    def test_valid_settings_file(self):
        settings_json = {
            "timeout": 5,
            "output_dir": "/tmp",
            "plugins": [
                {"tshark": ["-i", "lo"]},
                {"tshark": ["-i", "enp0s3"]}
            ]
        }
        with self.runner.isolated_filesystem() as dir:
            test_settings_file = os.path.join(dir, "test_settings_file.json")
            with open(test_settings_file, "w") as f:
                f.write(json.dumps(settings_json))
            result = self.runner.invoke(cli, ['--settings', test_settings_file])
            assert result.exit_code == 0
            assert "Using settings" in result.output or "Running with timeout=" in result.output
    
    def test_invalid_settings_file_json(self):
        with self.runner.isolated_filesystem() as dir:
            settings_path = os.path.join(dir, "bad_settings.json")
            with open(settings_path, "w") as f:
                f.write('{"timeout": 5, "output_dir": "output", plugins: [}')  # malformed JSON

            result = self.runner.invoke(cli, ['--settings', settings_path])
            assert result.exit_code != 0
            assert "Invalid JSON in settings file" in result.output

    def test_missing_settings_file(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['--settings', 'nonexistent.json'])
            assert result.exit_code != 0
            assert "Invalid value for '--settings'" in result.output

    def test_partial_settings_file(self):
        with self.runner.isolated_filesystem() as dir:
            partial_settings = {
                "timeout": 5  # missing output_dir and plugins
            }
            settings_path = os.path.join(dir, "partial.json")
            with open(settings_path, "w") as f:
                json.dump(partial_settings, f)

            result = self.runner.invoke(cli, ['--settings', settings_path])
            assert result.exit_code != 0
            assert "Missing required parameters" in result.output