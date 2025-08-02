from plugins.plugin import Plugin
import time

class PluginStub(Plugin):
    def run(self):
        time.sleep(0.5)
        return "I am finished"

    def is_applicable(self):
        return True


class BadPluginStub(Plugin):
    def run(self):
        time.sleep(0.5)
        raise Exception("Noob Plugin")
    
    def is_applicable(self):
        return True

class UnapplicablePluginStub(Plugin):
    def run(self):
        time.sleep(0.5)
        return "You should never hit this..."

    def is_applicable(self):
        return False
