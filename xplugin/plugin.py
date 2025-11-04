from xplugin.logger import xlogger

class Plugin:

    singleton = True
    separate_process = False
    continuous_run = False  # Whether the plugin should run continuously
    enabled = True
    tools = []
    is_built_in = False

    def __init__(self, built_in: bool = False):
        # Subclass initialization logic
        self.plugin_id = self.__class__.__name__
        self.name = self.__module__.split('.')[-1]
        self.description = "A plugin"
        self.shutdown_event = None  # Will be set by the plugin manager
        self.is_built_in = built_in
        pass


    def load_config(self, config: dict):
        return [(self, config)]


    def run(self):
        """Main plugin execution method. Override in subclasses."""
        return "Plugin is running"
    
    def is_shutdown_requested(self):
        """Check if shutdown has been requested"""
        return self.shutdown_event and self.shutdown_event.is_set()
    
    def wait_or_shutdown(self, timeout=1.0):
        """Wait for specified timeout or until shutdown is requested"""
        if self.shutdown_event:
            return self.shutdown_event.wait(timeout=timeout)
        else:
            import time
            time.sleep(timeout)
            return False
    
    def register_tool(self, tool: callable):
        # Logic to register a tool
        xlogger.debug(f"Registering tool: {tool.__name__}")
        self.tools.append(tool)

    def register_variable(self, var_name: str, value):
        setattr(self, var_name, value)
        xlogger.debug(f"Registered variable: {var_name} with value: {value}")

    def run_tool(self, tool_name, *args, **kwargs):
        xlogger.debug(f"Running tool: {tool_name} with args: {args} and kwargs: {kwargs}")
        xlogger.debug(self.tools)
        for tool in self.tools:
            if tool.__name__ == tool_name:
                return tool(*args, **kwargs)
        raise ValueError(f"Tool {tool_name} not found")
    
    def get_method_names(self):
        return [method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("__")]