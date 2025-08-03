from plugins.plugin import Plugin
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

TSHARK_PATH = Path("/usr/bin/tshark")
TSHARK_COMMAND = ["/usr/bin/tshark", "-i"]

class TsharkPlugin(Plugin):

    def __init__(self):
        self.is_multirunable = True
        self.is_configurable = True

    def is_applicable(self) -> bool:
        return TSHARK_PATH.exists()

    def run(self, timeout: float):
        return self.subprocess_helper(TSHARK_COMMAND, timeout)

    def configure_args(self, plugin_args: tuple | list[tuple]) -> None:
        if not self.is_configurable:
            Exception("Naughty Plugin, we shouldn't get here")
        if self.is_multirunable:
            # Have to figure out if it's trying to run multiple instances (i.e. tshark -i enpxxxx and tshark -i enpyyyy) 
            # or trying to append extra stuff into it... like tshark -i enpxxx -2
            # maybe the answer is in the CLI to instead of: " --plugin tshark enpxxxx enpyyyy" do: "--plugin tshark enpxxx --plugin tshark enpyyyy"
            # but I think I hate that...
            pass
        else:
            TSHARK_COMMAND.append(plugin_args)
