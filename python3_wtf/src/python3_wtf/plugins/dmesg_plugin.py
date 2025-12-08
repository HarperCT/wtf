from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

DMESG_PATH = Path("/usr/bin/dmesg")
DMESG_COMMAND = ["/usr/bin/dmesg", "-T"]


class DmesgPlugin(Plugin):

    def is_applicable(self) -> bool:
        return DMESG_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(DMESG_COMMAND, timeout)
