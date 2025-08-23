from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

LSMEM_PATH = Path("/usr/bin/lsmem")
LSMEM_COMMAND = ["/usr/bin/lsmem"]


class LSMEMPlugin(Plugin):

    def is_applicable(self) -> bool:
        return LSMEM_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(LSMEM_COMMAND, timeout)
