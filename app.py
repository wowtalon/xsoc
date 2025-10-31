from xplugin.plugin_manager import PluginManager
import logging
import signal
import sys
import os
import atexit
from threading import Thread, Event
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Global shutdown event
shutdown_event = Event()
active_threads = []

xsoc = {
    "core": {
        "version": "0.1.0",
        "plugins": {
            "built-in": [],
            "custom": []
        },
        "settings": {
            "debug": True,
            "host": "localhost",
            "port": 5000
        }
    }
}

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal, cleaning up threads...")
    shutdown_event.set()
    cleanup_threads()
    sys.exit(0)

def cleanup_threads():
    """Clean up all active threads"""
    logger.info("Cleaning up active threads...")
    shutdown_event.set()
    
    for thread in active_threads:
        if thread.is_alive():
            logger.debug(f"Waiting for thread {thread.name} to finish...")
            thread.join(timeout=5.0)  # Wait up to 5 seconds for each thread
            if thread.is_alive():
                logger.warning(f"Thread {thread.name} did not finish gracefully")
    
    active_threads.clear()
    logger.info("Thread cleanup completed")

def plugin_wrapper(plugin, *args, **kwargs):
    """Wrapper function to run plugins with shutdown event monitoring"""
    try:
        while not shutdown_event.is_set():
            result = plugin.run_plugin(*args, **kwargs)
            if not plugin.continuous_run:
                break
            shutdown_event.wait(timeout=1.0)  # Check for shutdown every second
    except Exception as e:
        logger.error(f"Error in plugin {plugin.name}: {e}")
    finally:
        logger.debug(f"Plugin {plugin.name} thread finished")

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Register cleanup function to run at exit
    atexit.register(cleanup_threads)

    xsoc_host = os.getenv("XSOC_HOST", "localhost")
    xsoc_port = int(os.getenv("XSOC_PORT", "5000"))
    
    try:
        manager = PluginManager()
        
        # Initialize built-in plugins
        built_in_plugins = manager.init_plugins_from_path('./plugins/built-in')
        xsoc["core"]["plugins"]["built-in"] = built_in_plugins
        # Initialize custom plugins
        custom_plugins = manager.init_plugins_from_path('./plugins/custom')
        xsoc["core"]["plugins"]["custom"] = custom_plugins
        
        for plugin in built_in_plugins:
            plugin.register_variable("xsoc_core", xsoc["core"])
            plugin.register_variable("shutdown_event", shutdown_event)
            
            if plugin.separate_process:
                if plugin.name == "WebPlugin":
                    thread = Thread(target=plugin_wrapper, args=(plugin,), kwargs={"port": xsoc_port}, daemon=True)
                else:
                    thread = Thread(target=plugin_wrapper, args=(plugin,), daemon=True)
                thread.name = f"Plugin-{plugin.name}"
                active_threads.append(thread)
                thread.start()
                logger.info(f"Started thread for plugin: {plugin.name}")
            else:
                plugin.run_plugin()
            logger.debug(active_threads)
        
        
        for plugin in custom_plugins:
            plugin.register_variable("xsoc_core", xsoc["core"])
            plugin.register_variable("shutdown_event", shutdown_event)
            
            if plugin.separate_process:
                thread = Thread(target=plugin_wrapper, args=(plugin,), daemon=True)
                thread.name = f"Plugin-{plugin.name}"
                active_threads.append(thread)
                thread.start()
                logger.info(f"Started thread for plugin: {plugin.name}")
            else:
                plugin.run_plugin()
        
        # Keep main thread alive if there are daemon threads running
        if active_threads:
            logger.info(f"Running with {len(active_threads)} plugin threads")
            try:
                while not shutdown_event.is_set() and any(t.is_alive() for t in active_threads):
                    shutdown_event.wait(timeout=1.0)
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                shutdown_event.set()
        
        logger.info("Main application finished")
        
    except Exception as e:
        logger.error(f"Error in main application: {e}")
        shutdown_event.set()
    finally:
        cleanup_threads()

if __name__ == "__main__":
    main()