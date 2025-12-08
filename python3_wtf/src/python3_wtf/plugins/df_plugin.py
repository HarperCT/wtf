from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

DF_PATH = Path("/usr/bin/df")
DF_COMMAND = ["/usr/bin/df", "-h"]


class DfPlugin(Plugin):

    def is_applicable(self) -> bool:
        return DF_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(DF_COMMAND, timeout)
