from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

IP_PATH = Path("/usr/sbin/ip")
IP_COMMAND = ["/usr/sbin/ip", "addr"]


class IpPlugin(Plugin):

    def is_applicable(self) -> bool:
        return IP_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(IP_COMMAND, timeout)
