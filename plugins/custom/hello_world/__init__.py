from xplugin.plugin import Plugin
import logging

logger = logging.getLogger(__name__)

def log_func(message: str, level: str = "info"):
    logger.log(logging._nameToLevel.get(level.upper(), 1), f"PluginManager [{level}]: {message}")

logger.debug("HelloWorld Plugin module loaded.")

class HelloWorldPlugin(Plugin):
    def run_plugin(self):
        log_func("Hello, World! This is the HelloWorldPlugin speaking.", level="info")
        return "Hello, World! This is the HelloWorldPlugin speaking."
    
    def say_hello_to(self, name: str) -> str:
        greeting = f"Hello, {name}! This is the HelloWorldPlugin speaking."
        log_func(greeting, level="info")
        return greeting
