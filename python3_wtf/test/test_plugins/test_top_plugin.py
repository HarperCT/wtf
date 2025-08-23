import unittest
from unittest.mock import patch
from python3_wtf.plugins.top_plugin import TopPlugin, TOP_COMMAND
from pathlib import Path

class TestTopPlugin(unittest.TestCase):
    def setUp(self):
        # github actions might scream at this... Eh, figure it out then
        if not Path("/usr/bin/top").exists:
            Path("/usr/bin/top").touch(exist_ok=True)
        self.plugin = TopPlugin()

    def test_is_applicable_true(self):
        assert self.plugin.is_applicable() is True

    def test_run_calls_subprocess_helper(self):
        mock_output = "mocked top output"
        
        with patch.object(self.plugin, "subprocess_helper", return_value=mock_output) as mock_helper:
            result = self.plugin.run(timeout=3.5)
            
            mock_helper.assert_called_once_with(TOP_COMMAND, 3.5)
            assert result == mock_output
