import logging
from python3_wtf.thread_runner import ThreadRunner
from python3_wtf.plugin_manager import PluginManager
from python3_wtf.package_outputs import archive_outputs
from pathlib import Path
logging.basicConfig(format='%(asctime)s - %(levelname)s \
                    - %(filename)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class WheresTheFault:
    def __init__(
        self,
        timeout: int,
        output_dir: Path,
        plugin_args: list[tuple[str, ...]]
    ):
        self.timeout = timeout
        self.output_dir = output_dir
        self.plugin_args = plugin_args

    def main_runner(self):
        plugin_detector = PluginManager(self.plugin_args)
        if plugin_detector.applicable_plugins == []:
            raise Exception("No applicable plugins! Try download some!")

        runner = ThreadRunner(
            timeout=self.timeout,
            plugins=plugin_detector.applicable_plugins)
        outputs = runner.run_threads()

        archive_outputs(outputs, "/tmp")
