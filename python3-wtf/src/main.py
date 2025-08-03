import logging
import thread_runner
import plugin_finder
import package_outputs
from pathlib import Path
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class WheresTheFault:
    def __init__(self, timeout: int, output_dir: Path, plugin_args: list[tuple]):
        self.timeout = timeout
        self.output_dir = output_dir
        self.plugin_args = plugin_args  # todo maybe type this nicer

    def main_runner(self):
        plugin_detector = plugin_finder.PluginDetector()
        if plugin_detector.applicable_plugins == []:
            Exception("No applicable plugins! Try download some!")

        plugin_detector.plug_in_plugin_args(self.plugin_args)
        runner = thread_runner.ThreadRunner(timeout=self.timeout, plugins=plugin_detector.applicable_plugins)
        outputs = runner.run_threads()

        package_outputs.archive_outputs(outputs, "/tmp")

