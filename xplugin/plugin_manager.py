from multiprocessing import Process, Event
from xplugin.logger import xlogger
import os



class PluginManager:

    shutdown_event = Event()
    active_threads = []
    active_processes = []
    plugins = {}
    startup_config = {}

    def __init__(self, plugin_config: dict = None):
        self.plugins = []
        self.running_plugins = []
        self.plugin_config = plugin_config or {}


    def __init__(self):
        pass


    def load_startup_config(self, path: str):
        """Load startup configuration from a YAML file"""
        import yaml
        xlogger.debug(f"Loading startup configuration from: {path}")
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
            self.startup_config = config.get("startups", [])
        except Exception as e:
            xlogger.error(f"Error loading startup configuration: {e}")


    def load_plugin(self, plugin_name, builtin: bool = False):
        """Dynamically load a plugin by name"""
        xlogger.debug(f"Loading plugin: {plugin_name}")
        try:
            module_name = f"plugins.builtin.{plugin_name}" if builtin else f"plugins.custom.{plugin_name}"
            module = __import__(module_name, fromlist=[''])
            plugin_class_name = ''.join([word.capitalize() for word in plugin_name.split('_')]) + 'Plugin'
            plugin_class = getattr(module, plugin_class_name, None)
            if plugin_class:
                plugin_instance = plugin_class(built_in=builtin)
                plugin_instance.register_variable("plugin_manager", self)
                self.register_plugin(plugin_instance, builtin=builtin)
                xlogger.debug(f"Plugin {plugin_name} loaded successfully")
                return plugin_instance
            else:
                xlogger.error(f"Plugin class {plugin_class_name} not found in module {module_name}")
                return None
        except Exception as e:
            xlogger.error(f"Error loading plugin {plugin_name}: {e}")
            return None
        
    def startup(self):
        """Run startup plugins"""
        xlogger.debug("Running startup plugins...")
        xlogger.debug(self.startup_config)
        try:
            for startup in self.startup_config:
                for startup_name, startup_info in startup.items():
                    xlogger.info(f"Starting up: {startup_name}")
                    plugin_name = startup_info.get("plugin")
                    context = startup_info.get("context", {})
                    xlogger.debug(f"Starting up plugin: {plugin_name} with context: {context}")
                    plugin = self.get_plugin(plugin_name)
                    if not plugin:
                        xlogger.debug(f"Plugin {plugin_name} not found, attempting to load...")
                        plugin = self.load_plugin(plugin_name)
                    if plugin:
                        xlogger.debug(f"Running startup plugin: {plugin.name}")
                        for _plugin, _kwargs in plugin.load_config(context):
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
                    else:
                        xlogger.error(f"Startup plugin {plugin_name} could not be loaded")
            if self.active_processes:
                xlogger.debug(f"Running with {len(self.active_processes)} plugin processes")
                try:
                    while not self.shutdown_event.is_set() and any(t.is_alive() for t in self.active_processes):
                        self.shutdown_event.wait(timeout=1.0)
                except KeyboardInterrupt:
                    xlogger.debug("KeyboardInterrupt received, shutting down...")
                    self.shutdown_event.set()
        except Exception as e:
            xlogger.error(f"Error during startup: {e}")
            self.shutdown_event.set()
        finally:
            self.cleanup_processes()


    def cleanup_processes(self):
        """Clean up all active processes"""
        xlogger.debug("Cleaning up active processes...")
        # self.shutdown_event.set()

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


    def register_plugin(self, plugin, builtin: bool = False):
        # Register a plugin and store its info to database
        xlogger.debug(f"Registering plugin: {plugin}")
        self.plugins[plugin.name] = {
            "instance": plugin,
            "builtin": builtin
        }


    def get_plugin(self, plugin_name: str):
        xlogger.debug(f"Retrieving plugin: {plugin_name}")
        for _plugin_name, plugin_info in self.plugins.items():
            xlogger.debug(f"Checking plugin: {plugin_info['instance'].name}")
            if plugin_info['instance'].name == plugin_name:
                return plugin_info['instance']
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
