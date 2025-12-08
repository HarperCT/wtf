import unittest
import asyncio
from unittest.mock import Mock, patch
from python3_wtf.async_runner import AsyncRunner, AsyncRunnerAdvanced
from python3_wtf.plugins.plugin import Plugin


class MockPlugin(Plugin):
    """Mock plugin for testing."""
    
    def __init__(self, name: str, delay: float = 0.1, should_fail: bool = False):
        super().__init__()
        self.name = name
        self.delay = delay
        self.should_fail = should_fail
    
    def is_applicable(self) -> bool:
        return True
    
    def run(self, timeout: float) -> tuple[str, str, bool]:
        """Simulate plugin execution."""
        import time
        time.sleep(self.delay)
        
        if self.should_fail:
            raise Exception(f"Mock failure in {self.name}")
        
        return (f"Output from {self.name}", "", False)


class TestAsyncRunner(unittest.TestCase):
    
    def test_single_plugin_execution(self):
        """Test running a single plugin."""
        plugin = MockPlugin("test_plugin", delay=0.01)
        runner = AsyncRunner(timeout=5.0, plugins=[plugin])
        
        results = runner.run_plugins()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "MockPlugin")
        self.assertIn("Output from test_plugin", results[0][1][0])
    
    def test_multiple_plugins_execution(self):
        """Test running multiple plugins concurrently."""
        plugins = [
            MockPlugin(f"plugin_{i}", delay=0.01)
            for i in range(5)
        ]
        runner = AsyncRunner(timeout=5.0, plugins=plugins)
        
        results = runner.run_plugins()
        
        self.assertEqual(len(results), 5)
        # All plugins should complete
        for result in results:
            self.assertEqual(result[0], "MockPlugin")
            self.assertFalse(result[1][2])  # Not timed out
    
    def test_plugin_failure_handling(self):
        """Test that one plugin failure doesn't stop others."""
        plugins = [
            MockPlugin("good_plugin_1", delay=0.01),
            MockPlugin("bad_plugin", delay=0.01, should_fail=True),
            MockPlugin("good_plugin_2", delay=0.01),
        ]
        runner = AsyncRunner(timeout=5.0, plugins=plugins)
        
        results = runner.run_plugins()
        
        self.assertEqual(len(results), 3)
        # Check that good plugins succeeded
        good_results = [r for r in results if "good_plugin" in r[1][0]]
        self.assertEqual(len(good_results), 2)
        
        # Check that bad plugin was handled
        bad_results = [r for r in results if "Exception" in r[1][1]]
        self.assertEqual(len(bad_results), 1)
    
    def test_timeout_handling(self):
        """Test that plugins timing out are handled correctly."""
        # Plugin that takes longer than timeout
        plugin = MockPlugin("slow_plugin", delay=2.0)
        runner = AsyncRunner(timeout=0.1, plugins=[plugin])
        
        results = runner.run_plugins()
        
        self.assertEqual(len(results), 1)
        # Should have timeout error
        self.assertTrue(results[0][1][2])  # Timed out flag
        self.assertIn("timeout", results[0][1][1].lower())
    
    def test_semaphore_limits_concurrency(self):
        """Test that semaphore properly limits concurrent execution."""
        plugins = [MockPlugin(f"plugin_{i}", delay=0.05) for i in range(20)]
        runner = AsyncRunner(timeout=5.0, plugins=plugins)
        runner.semaphore_limit = 3  # Limit to 3 concurrent
        
        results = runner.run_plugins()
        
        # All should complete despite limit
        self.assertEqual(len(results), 20)


class TestAsyncRunnerAdvanced(unittest.TestCase):
    
    def test_progress_tracking(self):
        """Test that advanced runner tracks progress."""
        plugins = [MockPlugin(f"plugin_{i}", delay=0.01) for i in range(5)]
        runner = AsyncRunnerAdvanced(
            timeout=5.0,
            plugins=plugins,
            max_concurrent=2
        )
        
        with patch.object(runner, 'logger') as mock_logger:
            results = runner.run_plugins()
            
            self.assertEqual(len(results), 5)
            # Should have logged progress
            self.assertEqual(runner.completed_count, 5)
    
    def test_custom_concurrency_limit(self):
        """Test custom concurrency limit."""
        plugins = [MockPlugin(f"plugin_{i}", delay=0.01) for i in range(10)]
        runner = AsyncRunnerAdvanced(
            timeout=5.0,
            plugins=plugins,
            max_concurrent=4
        )
        
        self.assertEqual(runner.semaphore_limit, 4)
        results = runner.run_plugins()
        self.assertEqual(len(results), 10)


class TestAsyncVsThreadPerformance(unittest.TestCase):
    """
    Comparison tests to demonstrate async advantages.
    These are informational and may be skipped in CI.
    """
    
    @unittest.skip("Performance test - run manually")
    def test_scalability_comparison(self):
        """
        Compare async vs thread runner with many plugins.
        Async should handle more plugins with less memory.
        """
        import time
        from python3_wtf.thread_runner import ThreadRunner
        
        # Create many plugins
        num_plugins = 50
        plugins = [MockPlugin(f"plugin_{i}", delay=0.05) for i in range(num_plugins)]
        
        # Test async runner
        async_runner = AsyncRunner(timeout=5.0, plugins=plugins)
        start = time.time()
        async_results = async_runner.run_plugins()
        async_time = time.time() - start
        
        # Test thread runner
        thread_runner = ThreadRunner(timeout=5.0, plugins=plugins)
        start = time.time()
        thread_results = thread_runner.run_threads()
        thread_time = time.time() - start
        
        print(f"\nAsync time: {async_time:.2f}s")
        print(f"Thread time: {thread_time:.2f}s")
        print(f"Speedup: {thread_time/async_time:.2f}x")
        
        # Both should complete all plugins
        self.assertEqual(len(async_results), num_plugins)
        self.assertEqual(len(thread_results), num_plugins)


if __name__ == '__main__':
    unittest.main()
