from xplugin.logger import xlogger
from threading import Thread, Event
import signal
import sys
import atexit
import os



class PluginManager:

    shutdown_event = Event()
    active_threads = []

    def __init__(self, plugin_config: dict = None):
        self.plugins = []
        self.plugin_config = plugin_config or {}
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Register cleanup function to run at exit
        atexit.register(self._cleanup_threads)

    def install_plugin(self, plugin_package: str):
        xlogger.debug(f"Installing plugin package: {plugin_package}")
        # unzip and install logic would go here
        # TODO: Implement plugin installation
        pass


    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        xlogger.debug("Received shutdown signal, cleaning up threads...")
        self.shutdown_event.set()
        self.cleanup_threads()
        sys.exit(0)


    def _cleanup_threads(self):
        """Clean up all active threads"""
        xlogger.debug("Cleaning up active threads...")
        self.shutdown_event.set()
        
        for thread in self.active_threads:
            if thread.is_alive():
                xlogger.debug(f"Waiting for thread {thread.name} to finish...")
                thread.join(timeout=5.0)  # Wait up to 5 seconds for each thread
                if thread.is_alive():
                    xlogger.warning(f"Thread {thread.name} did not finish gracefully")
        
        self.active_threads.clear()
        xlogger.debug("Thread cleanup completed")


    def _plugin_wrapper(self, plugin, *args, **kwargs):
        """Wrapper function to run plugins with shutdown event monitoring"""
        try:
            while not self.shutdown_event.is_set():
                plugin.run(*args, **kwargs)
                if not plugin.continuous_run:
                    break
                self.shutdown_event.wait(timeout=1.0)  # Check for shutdown every second
        except Exception as e:
            xlogger.error(f"Error in plugin {plugin.name}: {e}")
        finally:
            xlogger.debug(f"Plugin {plugin.name} thread finished")


    def run(self):
        xlogger.debug("Running all registered plugins...")
        xlogger.debug(self.plugin_config)
        try:
            for plugin in self.plugins:
                xlogger.debug(f"Starting plugin: {plugin.name}")
                if plugin.name in self.plugin_config and self.plugin_config[plugin.name].get('enabled', True) is False:
                    xlogger.debug(f"Skipping disabled plugin: {plugin.name}")
                    continue

                # plugin.register_variable("xsoc_core", xsoc["core"])
                plugin.register_variable("shutdown_event", self.shutdown_event)
                plugin.register_variable("plugin_manager", self)
                config = self.plugin_config.get(plugin.name, {})
                xlogger.debug(f"Loading config for plugin {plugin.name}: {config}")

                for _plugin, _kwargs in plugin.load_config(config):
                    xlogger.debug(f"Loaded config for plugin {_plugin.name}: {_plugin}, {_kwargs}")

                    if _plugin.separate_process:

                        thread = Thread(target=self._plugin_wrapper, args=(_plugin,), kwargs=_kwargs, daemon=True)
                        thread.name = f"Plugin-{_plugin.name}"
                        self.active_threads.append(thread)
                        thread.start()
                        xlogger.debug(f"Started thread for plugin: {plugin.name}")
                    else:
                        _plugin.run(**_kwargs)
            # Keep main thread alive if there are daemon threads running
            if self.active_threads:
                xlogger.debug(f"Running with {len(self.active_threads)} plugin threads")
                try:
                    while not self.shutdown_event.is_set() and any(t.is_alive() for t in self.active_threads):
                        self.shutdown_event.wait(timeout=1.0)
                except KeyboardInterrupt:
                    xlogger.debug("Keyboard interrupt received")
                    self.shutdown_event.set()
        except Exception as e:
            xlogger.error(f"Error in plugin manager: {e}")
            self.shutdown_event.set()
        finally:
            self._cleanup_threads()
    

    def register_plugin(self, plugin):
        # Register a plugin and store its info to database
        xlogger.debug(f"Registering plugin: {plugin}")
        self.plugins.append(plugin)
        # TODO: Store plugin info to database


    def get_plugin(self, plugin_name: str):
        for plugin in self.plugins:
            if plugin.name == plugin_name:
                return plugin
        return None

    def get_plugins(self):
        return self.plugins
    
    def clear_plugins(self):
        self.plugins = []

    def count_plugins(self):
        return len(self.plugins)
    
    def init_plugins_from_path(self, path: str, built_in: bool = False):
        xlogger.debug(f"Initializing plugins from path: {path}")
        # Register plugins from the given path
        for folder in os.listdir(path):
            folder_path = os.path.join(path, folder)
            if os.path.isdir(folder_path):
                try:
                    # Import the plugin module dynamically
                    plugin_name = ''.join([word.capitalize() for word in folder.split('_')]) + 'Plugin'
                    module_name = f"{path}/{folder}"
                    module_name = module_name.replace('/', '.').replace('\\', '.').lstrip('.')
                    xlogger.debug(f"Loading plugin module: {module_name}")
                    module = __import__(module_name, fromlist=[''])
                    # Instantiate the plugin class (assuming a class named 'Plugin' exists)
                    plugin_class = getattr(module, plugin_name, None)
                    xlogger.debug(f"Found plugin class: {plugin_class}")
                    if plugin_class:
                        plugin_instance = plugin_class(built_in=built_in)
                        self.register_plugin(plugin_instance)
                except Exception as e:
                    xlogger.error(f"Error loading plugin {folder}: {e}")

if __name__ == "__main__":
    manager = PluginManager()
    xlogger.debug("Plugin Manager initialized.")
    from plugin import Plugin
    class HelloWorldPlugin(Plugin):

        username = ""

        def greet(self):
            return "Hello, World!"
        
        def say_hello_to(self, name: str) -> str:
            self.username = name
            xlogger.debug(self.run_tool("testtool", self.plugin_id, self.username))
            return f"Hello, {name}!"
        
    def testtool(plugin_name: str, arg1: str) -> str:
        return "This is a test tool from {} with arg {}".format(plugin_name, arg1)
    manager.register_plugin(HelloWorldPlugin())
    hello = HelloWorldPlugin()
    hello.register_tool(testtool)
    xlogger.debug(hello.greet())  # Output: Hello, World!
    xlogger.debug(hello.get_method_names())  # Output: ['greet', 'say_hello_to', 'get_method_names', 'run']
    hello.say_hello_to("Talon")
