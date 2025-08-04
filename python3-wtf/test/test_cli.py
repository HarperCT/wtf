import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from pathlib import Path
from wtf_cli import cli


class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.patcher = patch("wtf_cli.WheresTheFault")
        self.mock_class = self.patcher.start()
        self.mock_instance = MagicMock()
        self.mock_class.return_value = self.mock_instance
        self.addCleanup(self.patcher.stop)

    def test_cli_required_options(self):
        with self.runner.isolated_filesystem():
            tmp_dir = Path("output")
            tmp_dir.mkdir()
            result = self.runner.invoke(cli, ['-t', '3', '-o', str(tmp_dir)])
            assert result.exit_code == 0
            assert "[WheresTheFault] Initializing WheresTheFault..." in result.output
            assert f"[WheresTheFault] Running with timeout=3, output_dir='{tmp_dir.resolve()}' and plugin_args=()" in result.output
            assert "[WheresTheFault] Done." in result.output
            assert self.mock_instance.main_runner.called

    def test_cli_missing_timeout(self):
        with self.runner.isolated_filesystem():
            tmp_dir = Path("output")
            tmp_dir.mkdir()
            result = self.runner.invoke(cli, ['-o', str(tmp_dir)])
            assert result.exit_code != 0
            assert "Missing option '-t' / '--timeout'" in result.output
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
