from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

LSOF_PATH = Path("/usr/bin/lsof")
LSOF_COMMAND = ["/usr/bin/lsof"]


class LsofPlugin(Plugin):

    def is_applicable(self) -> bool:
        return LSOF_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(LSOF_COMMAND, timeout)
