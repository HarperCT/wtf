from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

FREE_PATH = Path("/usr/bin/free")
FREE_COMMAND = ["/usr/bin/free", "-h"]


class FreePlugin(Plugin):

    def is_applicable(self) -> bool:
        return FREE_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(FREE_COMMAND, timeout)
