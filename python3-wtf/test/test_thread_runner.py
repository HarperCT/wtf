from thread_runner import ThreadRunner
from plugins.plugin import Plugin
import time

class PluginStub(Plugin):
    def run(self):
        time.sleep(0.5)
        return "I am finished"

class BadPluginStub(Plugin):
    def run(self):
        time.sleep(0.5)
        raise Exception("Noob Plugin")

class TestThreadRunner:

    def test_runs_multiple_threads(self):
        plugins = [PluginStub(), PluginStub(), PluginStub()]
        runner = ThreadRunner(5, plugins)
        results = runner.run_threads()
        assert results == ['I am finished', 'I am finished', 'I am finished']

    def test_returns_non_failed_threads_even_if_one_fails(self):
        plugins = [PluginStub(), BadPluginStub(), PluginStub(), BadPluginStub()]
        runner = ThreadRunner(5, plugins)
        results = runner.run_threads()
        assert results == ['I am finished', 'I am finished']
