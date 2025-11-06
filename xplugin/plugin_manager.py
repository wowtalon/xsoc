from multiprocessing import Process, Event
from xplugin.logger import xlogger
import os



class PluginManager:

    shutdown_event = Event()
    active_threads = []
    active_processes = []

    def __init__(self, plugin_config: dict = None):
        self.plugins = []
        self.running_plugins = []
        self.plugin_config = plugin_config or {}



    def cleanup_processes(self):
        """Clean up all active processes"""
        xlogger.debug("Cleaning up active processes...")
        self.shutdown_event.set()

        for process in self.active_processes:
            if process.is_alive():
                xlogger.debug(f"Waiting for process {process.name} to finish...")
                process.join(timeout=5.0)  # Wait up to 5 seconds for each process
                if process.is_alive():
                    xlogger.warning(f"Process {process.name} did not finish gracefully")
        
        self.active_processes.clear()
        xlogger.debug("Process cleanup completed")


    def _plugin_wrapper(self, plugin, shutdown_event, **kwargs):
        """Wrapper function to run plugins with shutdown event monitoring"""
        try:
            plugin.run(**kwargs)
        except Exception as e:
            xlogger.error(f"Error in plugin {plugin.name}: {e}")
        finally:
            xlogger.debug(f"Plugin {plugin.name} process finished")


    def run_plugin(self, plugin_name: str):
        """Run a specific plugin by name"""
        xlogger.debug(f"Running plugin: {plugin_name}")
        if plugin_name in self.running_plugins:
            xlogger.debug(f"Plugin {plugin_name} is already running")
            return
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            xlogger.error(f"Plugin {plugin_name} not found")
            raise ValueError(f"Plugin {plugin_name} not found")
        xlogger.debug(f"Starting plugin: {plugin.name}")
        if plugin.name in self.plugin_config and self.plugin_config[plugin.name].get('enabled', True) is False:
            xlogger.debug(f"Skipping disabled plugin: {plugin.name}")
            return

        xlogger.debug(f"Checking dependencies for plugin: {plugin.name}")
        xlogger.debug(f"Dependencies: {self.plugin_config[plugin.name].get('dependencies', [])}")
        self.check_dependencies(self.plugin_config[plugin.name].get('dependencies', []))

        # plugin.register_variable("xsoc_core", xsoc["core"])
        plugin.register_variable("shutdown_event", self.shutdown_event)
        plugin.register_variable("plugin_manager", self)
        config = self.plugin_config.get(plugin.name, {})
        xlogger.debug(f"Loading config for plugin {plugin.name}: {config}")

        for _plugin, _kwargs in plugin.load_config(config['params'] if 'params' in config else {}):

            if not _plugin:
                xlogger.debug(f"Skipping plugin as load_config returned None")
                continue

            if _plugin.separate_process:
                xlogger.debug(f"Plugin {_plugin.name} is set to run in a separate process")
                
                # Run plugin in a separate process
                process = Process(target=self._plugin_wrapper, args=(_plugin, self.shutdown_event, ), kwargs=_kwargs)
                process.name = f"Plugin-{_plugin.name}"
                self.active_processes.append(process)
                xlogger.debug(f"Starting process for plugin: {_plugin.name}")
                process.start()
                xlogger.debug(f"Started process for plugin: {_plugin.name}")
            else:
                _plugin.run(**_kwargs)
        self.running_plugins.append(plugin.name)


    def run_plugins(self, plugin_names: list):
        """Run a list of plugins"""
        xlogger.debug("Running all registered plugins...")
        xlogger.debug(self.plugin_config)
        if not plugin_names:
            xlogger.debug("No plugins specified to run.")
            return
        try:
            for plugin_name in plugin_names:
                self.run_plugin(plugin_name)
            # Keep main thread alive if there are daemon threads running
            if self.active_processes:
                xlogger.debug(f"Running with {len(self.active_processes)} plugin processes")
                try:
                    while not self.shutdown_event.is_set() and any(t.is_alive() for t in self.active_processes):
                        self.shutdown_event.wait(timeout=1.0)
                except KeyboardInterrupt:
                    xlogger.debug("KeyboardInterrupt received, shutting down...")
                    self.shutdown_event.set()
        except Exception as e:
            xlogger.error(f"Error in plugin manager: {e}")
            self.shutdown_event.set()
        finally:
            self.cleanup_processes()

    def run(self):
        xlogger.debug("Running all registered plugins...")
        xlogger.debug(self.plugin_config)
        self.run_plugins([plugin.name for plugin in self.plugins])
    

    def register_plugin(self, plugin):
        # Register a plugin and store its info to database
        xlogger.debug(f"Registering plugin: {plugin}")
        self.plugins.append(plugin)
        # TODO: Store plugin info to database


    def get_plugin(self, plugin_name: str):
        xlogger.debug(f"Retrieving plugin: {plugin_name}")
        for plugin in self.plugins:
            xlogger.debug(f"Checking plugin: {plugin.name}")
            if plugin.name == plugin_name:
                return plugin
        return None

    def get_plugins(self):
        return self.plugins
    
    def clear_plugins(self):
        self.plugins = []

    def count_plugins(self):
        return len(self.plugins)


    def check_dependencies(self, plugin_names):
        # Check and install dependencies for the plugin
        for plugin_name in plugin_names:
            xlogger.debug(f"Loading dependency: {plugin_name}")
            self.run_plugin(plugin_name)

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
                    xlogger.debug(f"Instantiating plugin: {plugin_name}")
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
