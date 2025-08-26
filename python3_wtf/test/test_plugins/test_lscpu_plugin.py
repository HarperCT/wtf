import unittest
from unittest.mock import patch
from python3_wtf.plugins.lscpu_plugin import LSCPUPlugin


class TestLSCPUPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = LSCPUPlugin()

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

        mock_helper.assert_called_once_with(["/usr/bin/lscpu"], 5.0)
        assert result == "mocked_output"
