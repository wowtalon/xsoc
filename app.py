import argparse
import sys
from xplugin.plugin_manager import PluginManager
from dotenv import load_dotenv
from xplugin.logger import xlogger
import os

load_dotenv()


xsoc = {
    "core": {
        "version": "0.2.0",
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


def main(config_path: str, plugin: str = None):
    
    config_file_path = os.getenv("XSOC_CONFIG_PATH", "config.yaml")
    if config_path:
        config_file_path = config_path
    xlogger.info(f"Loading configuration from {config_file_path}")
    config = load_config(config_file_path)

    if config.get("debug", False):
        xlogger.setLevel("debug")
        xlogger.debug("Debug mode is enabled")
    else:
        xlogger.setLevel("info")

    plugins = []
    for plugin_name, plugin_info in config.get("plugins", {}).items():
        if plugin_info.get("enabled", True) is False:
            xlogger.debug(f"Plugin {plugin_name} is disabled in configuration")
        else:
            plugins.append(
                {
                    "name": plugin_name,
                    "builtin": plugin_info.get("builtin", False),
                    "startup": plugin_info.get("startup", False),
                }
            )
    
    manager = PluginManager()

    for plugin in plugins:
        xlogger.info(f"Running startup plugin: {plugin}")
        manager.load_plugin(plugin["name"], builtin=plugin["builtin"])

    manager.load_startup_config('./example/plugin/startup.yaml')
    manager.startup()

    xlogger.debug(manager.plugins)       
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XSOC - eXtensible Service-Oriented Controller")
    parser.add_argument("--config", default="config.yaml", help="Path to the configuration file")
    parser.add_argument("--plugin", help="Specific plugin to run")
    args = parser.parse_args()
    main(args.config, args.plugin)