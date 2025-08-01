import concurrent.futures as cf
from plugins.plugin import Plugin
import logging
logger = logging.getLogger(__name__)

class ThreadRunner:
    def __init__(self, timeout: float, plugins: list[Plugin]):
        self.timeout = timeout
        self.plugins = plugins

    def run_threads(self) -> list:
        """
        Runs all the plugins .run() and appends their results in a grand list for usuage elsewhere
        """
        results = []
        with cf.ThreadPoolExecutor(max_workers=len(self.plugins)) as executor:
                # get all Plugin.run and submit them to the executor
                    # note need to be careful of agrs here... we can add them in the submit but I vote we handle all in the self. 
                    # of the specific plugin... shouldn't need anything here
                future_results = {executor.submit(plugin.run): plugin for plugin in self.plugins}
                
                for future in cf.as_completed(future_results):
                    item = future_results[future]
                    try:
                        result = future.result()
                        logger.debug(f"Received: {result}")
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Item {item.__class__} generated an exception: {e}")
        return results