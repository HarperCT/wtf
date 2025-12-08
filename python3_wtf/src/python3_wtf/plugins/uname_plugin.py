from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

UNAME_PATH = Path("/usr/bin/uname")
UNAME_COMMAND = ["/usr/bin/uname", "-a"]


class UnamePlugin(Plugin):

    def is_applicable(self) -> bool:
        return UNAME_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(UNAME_COMMAND, timeout)
