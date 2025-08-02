import concurrent.futures as cf
from plugins.plugin import Plugin
import logging
logger = logging.getLogger(__name__)

class ThreadRunner:
    def __init__(self, timeout: float, plugins: list[Plugin]):
        self.timeout = timeout  # unused atm but maybe eventually...
        self.plugins = plugins

    def run_threads(self) -> list[tuple[str, str]]:
        """
        Runs all the plugins .run() and appends their results in a grand list for usuage elsewhere
        """
        results = []
        with cf.ThreadPoolExecutor(max_workers=len(self.plugins)) as executor:
                # get all Plugin.run and submit them to the executor
                    # note need to be careful of agrs here... we can add them in the submit but I vote we handle all in the self. 
                    # of the specific plugin... shouldn't need anything here
                future_results = {executor.submit(plugin.run, plugin, self.timeout): plugin for plugin in self.plugins}
                
                for future in cf.as_completed(future_results, timeout=self.timeout+10):
                    item = future_results[future]
                    try:
                        result = future.result(timeout=self.timeout+10)
                        logger.debug(f"{item.__name__} Received: {result}")
                        results.append((item.__name__, result))
                    except TimeoutError:
                        logger.info(f"[TIMEOUT] {item.__name__} timed out, probably ok.")
                    except Exception as e:
                        logger.error(f"Item {item} generated an exception: {e}")
        return results