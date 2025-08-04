from plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

TOP_PATH = Path("/usr/bin/top")
TOP_COMMAND = ["/usr/bin/top", "-b"]

class TopPlugin(Plugin):

    def is_applicable(self) -> bool:
        return TOP_PATH.exists()
    
    def run(self, timeout: float):
        return self.subprocess_helper(TOP_COMMAND, timeout)

    