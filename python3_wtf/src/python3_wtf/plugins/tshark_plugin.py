from python3_wtf.plugins.plugin import Plugin
from pathlib import Path
import os
import grp
import logging

logger = logging.getLogger(__name__)

TSHARK_PATH = Path("/usr/bin/tshark")
TSHARK_COMMAND = ["/usr/bin/tshark"]


class TsharkPlugin(Plugin):

    def __init__(self):
        self.is_multirunable = True
        self.is_configurable = True
        self.command = TSHARK_COMMAND

    def is_applicable(self) -> bool:
        group_ids = os.getgroups()  # current user's associated group ids
        group_names = [grp.getgrgid(gid).gr_name for gid in group_ids]

        return TSHARK_PATH.exists() and \
            ("wireshark" in group_names or os.geteuid() == 0)

    def run(self, timeout: float):
        return self.subprocess_helper(self.command, timeout)

    def configure_args(self, plugin_args: list[str]) -> None:
        self.command = TSHARK_COMMAND + plugin_args
