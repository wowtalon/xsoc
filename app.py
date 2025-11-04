from xplugin.plugin_manager import PluginManager
from dotenv import load_dotenv
from xplugin.logger import xlogger
import os

load_dotenv()


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


def main():
    

    config_file_path = os.getenv("XSOC_CONFIG_PATH", "config.yaml")
    xlogger.debug(f"Loading configuration from {config_file_path}")
    config = load_config("config.yaml")

    if config.get("debug", False):
        xlogger.setLevel("debug")
        xlogger.debug("Debug mode is enabled")
    else:
        xlogger.setLevel("info")
    
    manager = PluginManager(config.get("plugins", {}))
    manager.init_plugins_from_path('./plugins/builtin', built_in=True)
    manager.init_plugins_from_path('./plugins/custom', built_in=False)
    manager.run()
        
        
        
    

if __name__ == "__main__":
    main()