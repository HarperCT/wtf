from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

AUSTIN_PATH = Path("/usr/bin/austin")
AUSTIN_COMMAND = ["/usr/bin/austin"]


class AustinPlugin(Plugin):

    def __init__(self):
        super().__init__()
        self.is_multirunable = True
        self.is_configurable = True
        self.command = AUSTIN_COMMAND

    def is_applicable(self) -> bool:
        return AUSTIN_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(self.command, timeout)

    def configure_args(self, plugin_args: list[str]) -> None:
        """
        Configure austin with PID and optional arguments.
        Expected format: austin <PID> [additional_args]
        Example: -p austin "1234" or -p austin "1234 -i 1000"
        """
        if not plugin_args:
            raise ValueError("Austin plugin requires at least a PID argument")
        
        # First arg should be the PID, rest are optional austin flags
        self.command = AUSTIN_COMMAND + ["-p"] + plugin_args
        logger.info(f"Austin configured with command: {self.command}")
