import unittest
from python3_wtf.plugins.plugin import Plugin


class DummyPlugin(Plugin):
    def is_applicable(self) -> bool:
        return True

    def run(self) -> str:
        return "dummy run output"


class TestPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = DummyPlugin()

    def test_initial_flags(self):
        self.assertFalse(self.plugin.is_multirunable)
        self.assertFalse(self.plugin.is_configurable)

    def test_configure_args_raises(self):
        with self.assertRaises(NotImplementedError) as cm:
            self.plugin.configure_args(("arg1", "arg2"))
        self.assertIn("Plugin does not support configuration", str(cm.exception))

    def test_subprocess_helper_success(self):
        stdout, stderr, timed_out = self.plugin.subprocess_helper(
            ["echo", "hello"],
            timeout=1
        )
        self.assertEqual(stdout.strip(), "hello")
        self.assertEqual(stderr, "")
        self.assertFalse(timed_out)

    def test_subprocess_helper_timeout(self):
        stdout, stderr, timed_out = self.plugin.subprocess_helper(
            ["sleep", "2"],
            timeout=0.5
        )
        self.assertTrue(timed_out)

    def test_subprocess_helper_invalid_command(self):
        stdout, stderr, timed_out = self.plugin.subprocess_helper(
            ["nonexistent_command"],
            timeout=1
        )
        self.assertTrue(timed_out)
        self.assertIn("Exception running command", stderr)
