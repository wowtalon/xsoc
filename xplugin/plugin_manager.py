import os
import logging

def log_func(message: str, level: str = "info"):
    logger.log(logging._nameToLevel.get(level.upper(), 1), f"PluginManager [{level}]: {message}")

logger = logging.getLogger(__name__)
log_func("Logger for PluginManager initialized.", level="debug")

class PluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def get_plugins(self):
        return self.plugins
    
    def clear_plugins(self):
        self.plugins = []

    def count_plugins(self):
        return len(self.plugins)
    
    def init_plugins_from_path(self, path: str):
        log_func(f"Initializing plugins from path: {path}", level="info")
        new_plugins = []  # Track only newly loaded plugins
        # Register plugins from the given path
        for folder in os.listdir(path):
            folder_path = os.path.join(path, folder)
            if os.path.isdir(folder_path):
                try:
                    # Import the plugin module dynamically
                    plugin_name = ''.join([word.capitalize() for word in folder.split('_')]) + 'Plugin'
                    module_name = f"{path}/{folder}"
                    module_name = module_name.replace('/', '.').replace('\\', '.').lstrip('.')
                    log_func(f"Loading plugin module: {module_name}", level="debug")
                    module = __import__(module_name, fromlist=[''])
                    # Instantiate the plugin class (assuming a class named 'Plugin' exists)
                    plugin_class = getattr(module, plugin_name, None)
                    if plugin_class:
                        plugin_instance = plugin_class()
                        self.register_plugin(plugin_instance)
                        new_plugins.append(plugin_instance)  # Add to new plugins list
                except Exception as e:
                    log_func(f"Error loading plugin {folder}: {e}", level="error")
        return new_plugins  # Return only newly loaded plugins

if __name__ == "__main__":
    manager = PluginManager()
    print("Plugin Manager initialized.")
    from plugin import Plugin
    class HelloWorldPlugin(Plugin):

        username = ""

        def greet(self):
            return "Hello, World!"
        
        def say_hello_to(self, name: str) -> str:
            self.username = name
            print(self.run_tool("testtool", self.plugin_id, self.username))
            return f"Hello, {name}!"
        
    def testtool(plugin_name: str, arg1: str) -> str:
        return "This is a test tool from {} with arg {}".format(plugin_name, arg1)
    manager.register_plugin(HelloWorldPlugin())
    hello = HelloWorldPlugin()
    hello.register_tool(testtool)
    print(hello.greet())  # Output: Hello, World!
    print(hello.get_method_names())  # Output: ['greet', 'say_hello_to', 'get_method_names', 'run']
    hello.say_hello_to("Talon")
