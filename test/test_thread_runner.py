from thread_runner import ThreadRunner
from plugins.plugin import Plugin
import time
import unittest

class PluginStub(Plugin):
    def run(self):
        time.sleep(0.5)
        return "I am finished"


class TestThreadRunner(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.plugins = [PluginStub(), PluginStub(), PluginStub()]

    def test_runs_multiple_threads(self):
        runner = ThreadRunner(5, self.plugins)
        results = runner.run_threads()
        print(results)
        assert results == ['I am finished', 'I am finished', 'I am finished']
