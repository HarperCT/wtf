from plugins.plugin import Plugin
from pathlib import Path

TOP_PATH = Path("/usr/bin/top")

class TopPlugin(Plugin):
    def __init__(self):
        pass
        
    def is_applicable(self) -> bool:
        return TOP_PATH.exists()

    def check_something_else_out(self):
        pass
    
    def run(self):
        # subprocess.run("/usr/bin/top param1 param2")
        pass

top = TopPlugin()
if top.is_applicable():
    top.check_something_else_out()
else:
    pass
