import logging
from python3_wtf.async_runner import AsyncRunner
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
        plugin_args: list[tuple[str, ...]],
        max_concurrent: int | None = None
    ):
        self.timeout = timeout
        self.output_dir = output_dir
        self.plugin_args = plugin_args
        self.max_concurrent = max_concurrent

    def main_runner(self):
        plugin_detector = PluginManager(self.plugin_args)
        if not plugin_detector.applicable_plugins:
            raise Exception("No applicable plugins! Try download some!")

        runner = AsyncRunner(
            timeout=self.timeout,
            plugins=plugin_detector.applicable_plugins,
            max_concurrent=self.max_concurrent
        )
        outputs = runner.run_plugins()

        # Use the user-specified output directory
        archive_path = archive_outputs(outputs, self.output_dir)
        logger.info(f"Results archived to: {archive_path}")
