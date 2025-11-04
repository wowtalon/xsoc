from xplugin.plugin_manager import PluginManager
from threading import Thread, Event
from dotenv import load_dotenv
from xplugin.logger import xlogger
import signal
import sys
import os
import atexit

load_dotenv()

# Global shutdown event
shutdown_event = Event()
active_threads = []

xsoc = {
    "core": {
        "version": "0.1.0",
        "plugins": [],
        "settings": {
            "debug": True,
            "host": "localhost",
            "port": 5000
        }
    }
}


def load_config(config_path: str):
    """Load configuration from a YAML file."""
    import yaml
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            xlogger.debug(f"Configuration loaded from {config_path}: {config}")
            return config
    except Exception as e:
        xlogger.error(f"Error loading configuration from {config_path}: {e}")
        return {}


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    xlogger.debug("Received shutdown signal, cleaning up threads...")
    shutdown_event.set()
    cleanup_threads()
    sys.exit(0)

def cleanup_threads():
    """Clean up all active threads"""
    xlogger.debug("Cleaning up active threads...")
    shutdown_event.set()
    
    for thread in active_threads:
        if thread.is_alive():
            xlogger.debug(f"Waiting for thread {thread.name} to finish...")
            thread.join(timeout=5.0)  # Wait up to 5 seconds for each thread
            if thread.is_alive():
                xlogger.warning(f"Thread {thread.name} did not finish gracefully")
    
    active_threads.clear()
    xlogger.debug("Thread cleanup completed")

def plugin_wrapper(plugin, *args, **kwargs):
    """Wrapper function to run plugins with shutdown event monitoring"""
    try:
        while not shutdown_event.is_set():
            result = plugin.run_plugin(*args, **kwargs)
            if not plugin.continuous_run:
                break
            shutdown_event.wait(timeout=1.0)  # Check for shutdown every second
    except Exception as e:
        xlogger.error(f"Error in plugin {plugin.name}: {e}")
    finally:
        xlogger.debug(f"Plugin {plugin.name} thread finished")

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Register cleanup function to run at exit
    atexit.register(cleanup_threads)

    config_file_path = os.getenv("XSOC_CONFIG_PATH", "config.yaml")
    xlogger.debug(f"Loading configuration from {config_file_path}")
    config = load_config("config.yaml")

    if config.get("debug", False):
        xlogger.setLevel("debug")
        xlogger.debug("Debug mode is enabled")
    else:
        xlogger.setLevel("info")
    
    try:
        manager = PluginManager()
        
        # Initialize built-in plugins
        built_in_plugins = manager.init_plugins_from_path('./plugins/builtin', built_in=True)
        # xsoc["core"]["plugins"]["builtin"] = {plugin.name: plugin for plugin in built_in_plugins}
        # xlogger.debug(f"Built-in plugins: {list(xsoc['core']['plugins']['builtin'])}")
        # Initialize custom plugins
        custom_plugins = manager.init_plugins_from_path('./plugins/custom', built_in=False)
        # xsoc["core"]["plugins"]["custom"] = {plugin.name: plugin for plugin in custom_plugins}
        xsoc["core"]["plugins"] = built_in_plugins + custom_plugins
        
        for plugin in xsoc["core"]["plugins"]:
            if plugin.name in config['plugins'] and config['plugins'][plugin.name].get('enabled', True) is False:
                xlogger.debug(f"Skipping disabled plugin: {plugin.name}")
                continue

            plugin.register_variable("xsoc_core", xsoc["core"])
            plugin.register_variable("shutdown_event", shutdown_event)
            
            if plugin.separate_process:
                if plugin.name == "web":
                    thread = Thread(target=plugin_wrapper, args=(plugin,), kwargs={"port": xsoc_port}, daemon=True)
                elif plugin.name == "workflow":
                    workflow_path = os.getenv("PLUGIN_WORKFLOW_PATH", "./data/workflows/")
                    xlogger.debug(f"Workflow path: {workflow_path}")
                    for config_file in os.listdir(workflow_path):
                        if config_file.endswith(".yaml") or config_file.endswith(".yml"):
                            config_path = os.path.join(workflow_path, config_file)
                            xlogger.debug(f"Starting workflow from config: {config_path}")
                            thread = Thread(target=plugin_wrapper, args=(plugin,), kwargs={"workflow_config_path": config_path}, daemon=True)
                            thread.name = f"Plugin-{plugin.name}-{config_file}"
                            active_threads.append(thread)
                            thread.start()
                    continue
                else:
                    thread = Thread(target=plugin_wrapper, args=(plugin,), daemon=True)
                thread.name = f"Plugin-{plugin.name}"
                active_threads.append(thread)
                thread.start()
                xlogger.debug(f"Started thread for plugin: {plugin.name}")
            else:
                plugin.run_plugin()
            # xlogger.debug(active_threads)
        
        
        # Keep main thread alive if there are daemon threads running
        if active_threads:
            xlogger.debug(f"Running with {len(active_threads)} plugin threads")
            try:
                while not shutdown_event.is_set() and any(t.is_alive() for t in active_threads):
                    shutdown_event.wait(timeout=1.0)
            except KeyboardInterrupt:
                xlogger.debug("Keyboard interrupt received")
                shutdown_event.set()
        
        xlogger.debug("Main application finished")
        
    except Exception as e:
        xlogger.error(f"Error in main application: {e}")
        shutdown_event.set()
    finally:
        cleanup_threads()

if __name__ == "__main__":
    main()