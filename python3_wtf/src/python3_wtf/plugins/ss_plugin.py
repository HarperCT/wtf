from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

SS_PATH = Path("/usr/sbin/ss")
SS_COMMAND = ["/usr/sbin/ss", "-tunapl"]


class SsPlugin(Plugin):

    def is_applicable(self) -> bool:
        return SS_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(SS_COMMAND, timeout)
