#!/usr/bin/env python3
"""
Comparison script to demonstrate AsyncRunner vs ThreadRunner performance.

Usage:
    python compare_runners.py [num_plugins]
"""

import sys
import time
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from python3_wtf.async_runner import AsyncRunner, AsyncRunnerAdvanced
from python3_wtf.thread_runner import ThreadRunner
from python3_wtf.plugin_manager import PluginManager

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def compare_runners(num_plugins: int = 20):
    """
    Compare AsyncRunner and ThreadRunner performance.
    
    Args:
        num_plugins: Number of plugins to simulate (default: 20)
    """
    logger.info(f"=== Comparing Runners with {num_plugins} Plugins ===\n")
    
    # Discover available plugins
    plugin_manager = PluginManager(plugin_args=[])
    available_plugins = plugin_manager.applicable_plugins
    
    if not available_plugins:
        logger.error("No plugins available! Install some Linux tools first.")
        return
    
    # Duplicate plugins to reach desired count
    plugins = []
    while len(plugins) < num_plugins:
        plugins.extend(available_plugins)
    plugins = plugins[:num_plugins]
    
    logger.info(f"Testing with {len(plugins)} plugin instances")
    logger.info(f"Unique plugins: {set(type(p).__name__ for p in plugins)}\n")
    
    timeout = 3.0
    
    # Test ThreadRunner
    logger.info("--- Testing ThreadRunner ---")
    thread_runner = ThreadRunner(timeout=timeout, plugins=plugins)
    
    start = time.time()
    thread_results = thread_runner.run_threads()
    thread_time = time.time() - start
    
    thread_success = sum(1 for r in thread_results if not r[1][2])
    logger.info(f"ThreadRunner completed in {thread_time:.2f}s")
    logger.info(f"Success: {thread_success}/{len(thread_results)}\n")
    
    # Test AsyncRunner
    logger.info("--- Testing AsyncRunner ---")
    async_runner = AsyncRunner(timeout=timeout, plugins=plugins)
    
    start = time.time()
    async_results = async_runner.run_plugins()
    async_time = time.time() - start
    
    async_success = sum(1 for r in async_results if not r[1][2])
    logger.info(f"AsyncRunner completed in {async_time:.2f}s")
    logger.info(f"Success: {async_success}/{len(async_results)}\n")
    
    # Test AsyncRunnerAdvanced
    logger.info("--- Testing AsyncRunnerAdvanced ---")
    advanced_runner = AsyncRunnerAdvanced(
        timeout=timeout,
        plugins=plugins,
        max_concurrent=8
    )
    
    start = time.time()
    advanced_results = advanced_runner.run_plugins()
    advanced_time = time.time() - start
    
    advanced_success = sum(1 for r in advanced_results if not r[1][2])
    logger.info(f"AsyncRunnerAdvanced completed in {advanced_time:.2f}s")
    logger.info(f"Success: {advanced_success}/{len(advanced_results)}\n")
    
    # Summary
    logger.info("=== Summary ===")
    logger.info(f"ThreadRunner:        {thread_time:.2f}s")
    logger.info(f"AsyncRunner:         {async_time:.2f}s")
    logger.info(f"AsyncRunnerAdvanced: {advanced_time:.2f}s")
    
    if async_time < thread_time:
        speedup = thread_time / async_time
        logger.info(f"\nAsyncRunner is {speedup:.2f}x faster!")
    else:
        logger.info(f"\nThreadRunner was faster (small plugin count)")
    
    # Memory estimation
    thread_memory_mb = len(plugins) * 8  # ~8MB per thread
    async_memory_kb = len(plugins) * 1   # ~1KB per coroutine
    
    logger.info(f"\nEstimated Memory Usage:")
    logger.info(f"ThreadRunner:  ~{thread_memory_mb}MB")
    logger.info(f"AsyncRunner:   ~{async_memory_kb}KB")
    logger.info(f"Memory saved:  ~{thread_memory_mb * 1024 / async_memory_kb:.0f}x")


def main():
    """Main entry point."""
    num_plugins = 20
    
    if len(sys.argv) > 1:
        try:
            num_plugins = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid number: {sys.argv[1]}")
            sys.exit(1)
    
    if num_plugins < 1 or num_plugins > 100:
        logger.error("Number of plugins must be between 1 and 100")
        sys.exit(1)
    
    try:
        compare_runners(num_plugins)
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
