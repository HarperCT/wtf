import unittest
from unittest.mock import patch
from python3_wtf.plugins.austin_plugin import AustinPlugin


class TestAustinPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = AustinPlugin()

    def test_is_applicable_when_exists(self):
        with patch("pathlib.Path.exists", return_value=True):
            assert self.plugin.is_applicable() is True

    def test_is_applicable_when_missing(self):
        with patch("pathlib.Path.exists", return_value=False):
            assert self.plugin.is_applicable() is False

    def test_run_calls_subprocess_helper(self):
        with patch.object(
            self.plugin,
            "subprocess_helper",
            return_value="mocked_output"
        ) as mock_helper:
            result = self.plugin.run(timeout=5.0)

        mock_helper.assert_called_once_with(self.plugin.command, 5.0)
        assert result == "mocked_output"

    def test_configure_args_with_pid_only(self):
        self.plugin.configure_args(["1234"])
        assert self.plugin.command == ["/usr/bin/austin", "-p", "1234"]

    def test_configure_args_with_pid_and_options(self):
        self.plugin.configure_args(["1234", "-i", "1000"])
        assert self.plugin.command == ["/usr/bin/austin", "-p", "1234", "-i", "1000"]

    def test_configure_args_raises_without_args(self):
        with self.assertRaises(ValueError) as context:
            self.plugin.configure_args([])
        assert "requires at least a PID argument" in str(context.exception)

    def test_is_multirunable(self):
        assert self.plugin.is_multirunable is True

    def test_is_configurable(self):
        assert self.plugin.is_configurable is True
