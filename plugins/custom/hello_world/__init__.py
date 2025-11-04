from xplugin.plugin import Plugin
from xplugin.logger import xlogger


xlogger.debug("HelloWorld Plugin module loaded.")

class HelloWorldPlugin(Plugin):
    def run_plugin(self):
        xlogger.info("Hello, World! This is the HelloWorldPlugin speaking.")
        return "Hello, World! This is the HelloWorldPlugin speaking."
    
    def say_hello_to(self, name: str) -> str:
        greeting = f"Hello, ------{name}------! This is the HelloWorldPlugin speaking."
        xlogger.info(greeting)
        return greeting
