from python3_wtf.thread_runner import ThreadRunner
from common_test_functions import PluginStub, BadPluginStub

class TestThreadRunner:

    def test_runs_multiple_threads(self):
        plugins = [PluginStub(), PluginStub(), PluginStub()]
        runner = ThreadRunner(5, plugins)
        results = runner.run_threads()
        assert results == [('PluginStub', 'I am finished'), ('PluginStub', 'I am finished'), ('PluginStub', 'I am finished')]

    def test_returns_non_failed_threads_even_if_one_fails(self):
        plugins = [PluginStub(), BadPluginStub(), PluginStub(), BadPluginStub()]
        runner = ThreadRunner(5, plugins)
        results = runner.run_threads()
        assert results == [('PluginStub', 'I am finished'), ('PluginStub', 'I am finished')]
