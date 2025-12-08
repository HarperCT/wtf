from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

PS_PATH = Path("/usr/bin/ps")
PS_COMMAND = ["/usr/bin/ps", "aux"]


class PsPlugin(Plugin):

    def is_applicable(self) -> bool:
        return PS_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(PS_COMMAND, timeout)
