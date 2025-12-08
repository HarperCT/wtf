from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

UPTIME_PATH = Path("/usr/bin/uptime")
UPTIME_COMMAND = ["/usr/bin/uptime"]


class UptimePlugin(Plugin):

    def is_applicable(self) -> bool:
        return UPTIME_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(UPTIME_COMMAND, timeout)
