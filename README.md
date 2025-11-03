# XSOC - eXtensible Security Operations Center

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/wowtalon/xsoc)

[中文版本](README_zh.md) | English

## Overview

XSOC (eXtensible Security Operations Center) is a modern, plugin-based security operations platform designed to provide comprehensive security monitoring, incident response, and threat management capabilities. Built with Python and featuring a flexible plugin architecture, XSOC allows organizations to customize and extend their security operations according to their specific needs.

## Features

- **🔌 Plugin Architecture**: Extensible plugin system supporting both built-in and custom plugins
- **🌐 Web Interface**: Modern web-based dashboard with responsive design
- **⚙️ Workflow Engine**: Automated workflow processing with YAML configuration
- **🔧 Tool Integration**: Dynamic tool loading and execution framework
- **📊 Real-time Monitoring**: Live security event monitoring and alerting
- **🛡️ SOC Operations**: Comprehensive security operations center functionality
- **⚡ Multi-threading**: Efficient concurrent plugin execution
- **🔄 Graceful Shutdown**: Proper resource cleanup and thread management

## Architecture

```
xsoc/
├── app.py                 # Main application entry point
├── main.py               # Alternative entry point
├── xplugin/              # Plugin framework
│   ├── plugin.py         # Base plugin class
│   ├── plugin_manager.py # Plugin management system
│   └── main.py          # Plugin framework entry
├── plugins/              # Plugin directory
│   ├── builtin/         # Built-in plugins
│   │   ├── web/         # Web interface plugin
│   │   └── workflow/    # Workflow engine plugin
│   └── custom/          # Custom user plugins
├── data/                # Data storage
└── example/            # Example configurations
```

## Quick Start

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wowtalon/xsoc.git
   cd xsoc
   ```

2. **Install dependencies:**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Using uv (recommended)
   uv sync
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

### Environment Variables

Create a `.env` file in the project root:

```env
XSOC_HOST=localhost
XSOC_PORT=5000
XSOC_DEBUG=true
```

## Plugin Development

### Creating a Custom Plugin

1. **Create plugin directory:**
   ```bash
   mkdir plugins/custom/my_plugin
   ```

2. **Create plugin class:**
   ```python
   # plugins/custom/my_plugin/__init__.py
   from xplugin.plugin import Plugin
   
   class MyPlugin(Plugin):
       def __init__(self):
           super().__init__()
           self.name = "MyPlugin"
           self.description = "My custom security plugin"
           self.separate_process = False
           
       def run_plugin(self):
           # Your plugin logic here
           return "MyPlugin is running"
   ```

### Plugin Configuration

Plugins can be configured with the following attributes:

- `separate_process`: Run plugin in separate thread (default: False)
- `continuous_run`: Keep plugin running continuously (default: False)
- `singleton`: Ensure only one instance (default: True)

### Built-in Plugins

#### Web Plugin

Provides a modern web interface with:
- Dashboard overview
- SOC operations panel
- Plugin management interface
- Settings configuration

Access at: `http://localhost:5000`

#### Workflow Plugin

Enables automated workflow processing:
- YAML-based workflow definitions
- Dynamic tool loading
- Step-by-step execution
- Error handling and logging

## API Reference

### Plugin Base Class

```python
class Plugin:
    def __init__(self):
        # Plugin initialization
        
    def run_plugin(self):
        # Main plugin execution method
        
    def register_tool(self, tool: callable):
        # Register a tool function
        
    def register_variable(self, var_name: str, value):
        # Register a variable
        
    def is_shutdown_requested(self):
        # Check if shutdown is requested
```

### Plugin Manager

```python
class PluginManager:
    def register_plugin(self, plugin):
        # Register a plugin instance
        
    def init_plugins_from_path(self, path: str):
        # Load plugins from directory
        
    def get_plugins(self):
        # Get all registered plugins
```

## Configuration

### Application Configuration

The main configuration is stored in the `xsoc` dictionary in `app.py`:

```python
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
```

### Plugin Configuration

Plugins can access the core configuration through the `xsoc_core` variable:

```python
def run_plugin(self):
    version = self.xsoc_core["version"]
    debug_mode = self.xsoc_core["settings"]["debug"]
```

## Development

### Setting up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wowtalon/xsoc.git
   cd xsoc
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=xplugin

# Run specific test
python -m pytest xplugin/tests/test_sample.py
```

### Code Style

This project follows PEP 8 style guidelines. Format code using:

```bash
black .
flake8 .
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Ensure all tests pass: `python -m pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [Wiki](https://github.com/wowtalon/xsoc/wiki)
- **Issues**: [GitHub Issues](https://github.com/wowtalon/xsoc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/wowtalon/xsoc/discussions)

## Changelog

### v0.1.0 (Current)
- Initial release
- Plugin architecture implementation
- Web interface plugin
- Workflow engine plugin
- Multi-threading support
- Graceful shutdown handling

## Roadmap

- [ ] Advanced plugin dependency management
- [ ] Plugin marketplace and registry
- [ ] Enhanced web UI with real-time updates
- [ ] Database integration for persistent storage
- [ ] REST API for external integrations
- [ ] Container deployment support
- [ ] Advanced workflow features
- [ ] Security scanning and vulnerability management
- [ ] Threat intelligence integration
- [ ] Incident response automation

---

Made with ❤️ by the XSOC Team