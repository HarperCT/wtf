import unittest
from unittest.mock import patch, MagicMock

from python3_wtf.plugins.tshark_plugin import TsharkPlugin


class TestTsharkPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = TsharkPlugin()

    @patch("pathlib.Path.exists", return_value=True)
    @patch("os.getgroups")
    @patch("grp.getgrgid")
    @patch("os.geteuid")
    def test_is_applicable_true_when_in_group(self, mock_geteuid, mock_getgrgid, mock_getgroups, mock_exists):
        # Setup mocks for group membership
        mock_getgroups.return_value = [1000, 1001]
        mock_getgrgid.side_effect = lambda gid: MagicMock(gr_name="wireshark" if gid == 1000 else "othergroup")
        mock_geteuid.return_value = 1001  # non-root user

        applicable = self.plugin.is_applicable()
        assert applicable is True

    @patch("pathlib.Path.exists", return_value=True)
    @patch("os.getgroups")
    @patch("grp.getgrgid")
    @patch("os.geteuid")
    def test_is_applicable_true_when_root(self, mock_geteuid, mock_getgrgid, mock_getgroups, mock_exists):
        mock_getgroups.return_value = []
        mock_getgrgid.side_effect = lambda gid: MagicMock(gr_name="nogroup")
        mock_geteuid.return_value = 0  # root user

        applicable = self.plugin.is_applicable()
        assert applicable is True

    @patch("pathlib.Path.exists", return_value=False)
    @patch("os.getgroups")
    @patch("grp.getgrgid")
    @patch("os.geteuid")
    def test_is_applicable_false_when_no_path(self, mock_geteuid, mock_getgrgid, mock_getgroups, mock_exists):
        # Even if groups or root, missing tshark binary disables applicability
        mock_getgroups.return_value = [1000]
        mock_getgrgid.return_value = MagicMock(gr_name="wireshark")
        mock_geteuid.return_value = 1000

        applicable = self.plugin.is_applicable()
        assert applicable is False

    @patch.object(TsharkPlugin, "subprocess_helper")
    def test_run_calls_subprocess_helper(self, mock_subprocess_helper):
        timeout = 42.0
        mock_subprocess_helper.return_value = "result"
        result = self.plugin.run(timeout)
        mock_subprocess_helper.assert_called_once_with(self.plugin.command, timeout)
        assert result == "result"

    def test_configure_args_appends_pased_in_args(self):
        extra_args = ["-i", "enpxxx"]
        self.plugin.configure_args(extra_args)
        assert self.plugin.command == ["/usr/bin/tshark", "-i", "enpxxx"]
