from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

LSCPU_PATH = Path("/usr/bin/lscpu")
LSCPU_COMMAND = ["/usr/bin/lscpu"]

class LSCPUPlugin(Plugin):

    def is_applicable(self) -> bool:
        return LSCPU_PATH.exists()
    
    def run(self, timeout: float):
        return self.subprocess_helper(LSCPU_COMMAND, timeout)

