import logging
import thread_runner
import plugin_finder
import package_outputs
from pathlib import Path
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class WheresTheFault:
    def __init__(self, timeout: int, output_dir: Path):
        self.timeout = timeout
        self.output_dir = output_dir

    def main_runner(self):
        plugin_detector = plugin_finder.PluginDetector()
        runner = thread_runner.ThreadRunner(timeout=self.timeout, plugins=plugin_detector.applicable_plugins)
        outputs = runner.run_threads()

        package_outputs.archive_outputs(outputs, "/tmp")
