import concurrent.futures as cf
from python3_wtf.plugins.plugin import Plugin
import logging
import os

logger = logging.getLogger(__name__)


class ThreadRunner:
    def __init__(self, timeout: float, plugins: list[Plugin]):
        self.timeout = timeout
        self.plugins = plugins

    def run_threads(self) -> list[tuple[str, str]]:
        """
        Runs all the plugins .run() and appends their
        results in a grand list for usuage elsewhere
        """
        results = []
        # Cap max_workers to reasonable limit (CPU count * 2 or plugin count)
        max_workers = min(len(self.plugins), (os.cpu_count() or 4) * 2)
        
        with cf.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # get all Plugin.run and submit them to the executor
            future_to_plugin = {
                executor.submit(
                    plugin.run,
                    self.timeout
                ): plugin for plugin in self.plugins
            }

            try:
                # Add buffer to overall timeout to allow plugin cleanup
                overall_timeout = self.timeout + 5
                
                for future in cf.as_completed(
                    future_to_plugin,
                    timeout=overall_timeout
                ):
                    plugin = future_to_plugin[future]
                    plugin_name = type(plugin).__name__
                    
                    try:
                        # Plugin already handles timeout internally, no need for extra timeout here
                        result = future.result()
                        logger.debug(f"{plugin_name} completed successfully")
                        results.append((plugin_name, result))
                    except cf.TimeoutError:
                        logger.error(f"{plugin_name} timed out after {self.timeout}s")
                        results.append((plugin_name, ("", f"[Timeout after {self.timeout}s]", True)))
                    except Exception as e:
                        logger.error(f"{plugin_name} generated an exception: {e}")
                        results.append((plugin_name, ("", f"[Exception: {e}]", True)))
                        
            except cf.TimeoutError:
                logger.error(f"Overall execution timed out after {overall_timeout}s")
                # Cancel any remaining futures
                for future in future_to_plugin:
                    future.cancel()
            except KeyboardInterrupt:
                logger.warning("Execution interrupted by user")
                # Cancel all futures on interrupt
                for future in future_to_plugin:
                    future.cancel()
                raise
                
        return results
