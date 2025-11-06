# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Plugin marketplace integration
- Advanced workflow features and conditional logic
- REST API for external integrations
- Container deployment support
- Real-time event streaming
- Database integration for persistent storage
- Enhanced web UI with real-time updates
- Security scanning and vulnerability management

## [0.2.0] - 2025-11-06

### Added
- Jinja2 template parsing for dynamic parameter resolution in workflows
- Enhanced workflow engine with context variable support
- Colored logging system with level-based color coding (xLogger class)
- Dynamic tool loading and execution framework
- Comprehensive workflow tools library with utility functions:
  - Conditional operations (`if_condition_met`, `case_condition_met`)
  - Type checking (`is_true`, `is_false`, `is_none`)
  - Type conversion (`convert_to_string`, `convert_to_int`)
  - String operations (`concatenate_strings`)
  - Utility functions (`print_message`, `loop_until_condition_met`)
- Environment variable and step result referencing in workflows using `{{ }}` syntax
- Plugin dictionary structure for improved plugin management and lookup
- Enhanced documentation with workflow examples and API references

### Changed
- Plugin storage structure from lists to dictionaries for O(1) lookup performance
- Workflow parameter resolution now uses Jinja2 templating engine
- Enhanced workflow step execution with better error handling and context management
- Improved plugin initialization and registration process
- Plugin access pattern changed to dictionary-based lookup by name
- Workflow engine now supports complex parameter interpolation

### Fixed
- Plugin duplicate registration issue resolved through improved plugin manager
- Thread management and cleanup improvements for graceful shutdown
- Workflow context variable resolution and parameter passing
- Plugin wrapper error handling and logging improvements

### Technical Improvements
- Added xLogger class with colored console output for better debugging
- Enhanced plugin wrapper with comprehensive error handling
- Improved workflow configuration parsing with YAML validation
- Better separation of built-in and custom plugin handling
- Dynamic module importing for workflow tools
- Context-aware parameter resolution in workflow steps

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