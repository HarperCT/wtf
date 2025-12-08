from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

LSPCI_PATH = Path("/usr/bin/lspci")
LSPCI_COMMAND = ["/usr/bin/lspci", "-v"]


class LspciPlugin(Plugin):

    def is_applicable(self) -> bool:
        return LSPCI_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(LSPCI_COMMAND, timeout)
