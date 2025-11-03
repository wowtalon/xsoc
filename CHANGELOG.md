# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Plugin marketplace integration
- Advanced workflow features
- REST API for external integrations
- Container deployment support
- Real-time event streaming

### Changed
- Improved plugin loading performance
- Enhanced error handling across the system
- Updated web interface design

### Deprecated
- Legacy plugin configuration format

### Security
- Enhanced input validation
- Improved authentication mechanisms

## [0.1.0] - 2025-11-03

### Added
- Initial release of XSOC platform
- Core plugin architecture with dynamic loading
- Plugin Manager for built-in and custom plugins
- Base Plugin class with standardized interface
- Web Plugin with modern responsive interface
  - Dashboard overview page
  - SOC operations panel
  - Plugin management interface  
  - Settings configuration page
- Workflow Plugin for automated task processing
  - YAML-based workflow definitions
  - Dynamic tool loading and execution
  - Step-by-step workflow processing
- Multi-threaded plugin execution support
- Graceful shutdown handling with proper cleanup
- Signal handling for SIGINT and SIGTERM
- Environment-based configuration with .env support
- Comprehensive logging system
- Thread-safe plugin registration and management
- Jinja2 template engine integration
- Flask web framework integration
- Built-in plugin discovery and loading
- Custom plugin support
- Plugin variable registration system
- Tool registration and execution framework

### Framework Features
- Plugin separation into built-in and custom categories
- Thread management with daemon threads
- Shutdown event propagation
- Plugin lifecycle management
- Configuration injection into plugins
- Error handling and recovery
- Resource cleanup on shutdown

### Web Interface Features
- Responsive navigation menu
- Mobile-friendly hamburger menu
- Modern card-based layout
- Template inheritance support
- Route handling for all main sections
- Static file serving
- Error page handling

### Developer Experience
- Comprehensive documentation (English and Chinese)
- Plugin development guidelines
- API reference documentation
- Example plugin implementations
- Development setup instructions
- Contributing guidelines
- Code style enforcement
- Testing framework setup

### Technical Implementation
- Python 3.12+ compatibility
- Flask web framework
- Jinja2 templating
- PyYAML configuration
- python-dotenv environment management
- Threading and signal handling
- Dynamic module importing
- Plugin class introspection
- Graceful error handling

### Documentation
- Complete README.md in English
- Complete README_zh.md in Chinese
- CONTRIBUTING.md with development guidelines
- LICENSE file with MIT license
- Inline code documentation
- Plugin development examples

[Unreleased]: https://github.com/wowtalon/xsoc/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/wowtalon/xsoc/releases/tag/v0.1.0