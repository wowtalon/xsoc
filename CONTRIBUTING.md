# Contributing to XSOC

Thank you for your interest in contributing to XSOC! This document provides guidelines and information for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Plugin Development](#plugin-development)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature/fix
5. Make your changes
6. Test your changes
7. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/xsoc.git
cd xsoc

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if applicable)
pip install -r requirements-dev.txt

# Run tests to verify setup
python -m pytest
```

## How to Contribute

### Types of Contributions

- **Bug Reports**: Submit detailed bug reports with reproduction steps
- **Feature Requests**: Propose new features with clear use cases
- **Code Contributions**: Bug fixes, new features, performance improvements
- **Documentation**: Improve existing docs or add new documentation
- **Plugin Development**: Create new plugins or enhance existing ones

### Reporting Bugs

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the bug
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, XSOC version
- **Logs**: Relevant log files or error messages

### Suggesting Features

When suggesting features:

- **Use Case**: Explain why this feature is needed
- **Description**: Detailed description of the proposed feature
- **Examples**: Provide examples of how it would be used
- **Alternatives**: Consider alternative solutions

## Plugin Development

### Creating New Plugins

1. **Plugin Structure**:
   ```
   plugins/custom/my_plugin/
   ├── __init__.py
   ├── tools.py (optional)
   ├── config.yaml (optional)
   └── README.md
   ```

2. **Plugin Template**:
   ```python
   from xplugin.plugin import Plugin
   
   class MyPlugin(Plugin):
       def __init__(self):
           super().__init__()
           self.name = "MyPlugin"
           self.description = "Description of my plugin"
           self.version = "1.0.0"
           
       def run_plugin(self):
           # Plugin implementation
           pass
   ```

3. **Plugin Guidelines**:
   - Follow the base Plugin class interface
   - Implement proper error handling
   - Add comprehensive logging
   - Include documentation
   - Write unit tests

### Plugin Best Practices

- **Resource Management**: Properly clean up resources
- **Thread Safety**: Ensure thread-safe operations if needed
- **Configuration**: Use configuration files for settings
- **Logging**: Use the logging framework consistently
- **Error Handling**: Handle errors gracefully with meaningful messages

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and small
- Use type hints where appropriate

### Code Formatting

```bash
# Format code with black
black .

# Check style with flake8
flake8 .

# Sort imports with isort
isort .
```

### Naming Conventions

- **Files**: Use lowercase with underscores (`my_plugin.py`)
- **Classes**: Use PascalCase (`MyPlugin`)
- **Functions/Variables**: Use snake_case (`run_plugin`)
- **Constants**: Use UPPER_CASE (`MAX_RETRIES`)

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=xplugin --cov-report=html

# Run specific test file
python -m pytest tests/test_plugin.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests

- Write unit tests for new functionality
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies
- Aim for high test coverage

### Test Structure

```python
import pytest
from xplugin.plugin import Plugin

class TestMyPlugin:
    def setup_method(self):
        self.plugin = MyPlugin()
    
    def test_plugin_initialization(self):
        assert self.plugin.name == "MyPlugin"
    
    def test_plugin_run(self):
        result = self.plugin.run_plugin()
        assert result is not None
```

## Documentation

### Documentation Standards

- Use clear and concise language
- Include code examples
- Keep documentation up to date
- Use proper Markdown formatting

### Types of Documentation

- **API Documentation**: Document all public methods and classes
- **User Guides**: Step-by-step instructions for users
- **Developer Guides**: Technical documentation for developers
- **Plugin Documentation**: Specific documentation for plugins

## Pull Request Process

### Before Submitting

1. **Update your branch**: Sync with the latest main branch
2. **Run tests**: Ensure all tests pass
3. **Check formatting**: Run code formatters
4. **Update documentation**: Update relevant documentation
5. **Test locally**: Test your changes thoroughly

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings or errors
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers review the code
3. **Feedback**: Address any feedback or requested changes
4. **Approval**: Get approval from maintainers
5. **Merge**: Changes are merged into main branch

### Commit Message Guidelines

Use clear and descriptive commit messages:

```
feat: add new workflow plugin
fix: resolve thread cleanup issue
docs: update plugin development guide
test: add unit tests for plugin manager
refactor: improve error handling in web plugin
```

## Getting Help

- **Documentation**: Check the [Wiki](https://github.com/wowtalon/xsoc/wiki)
- **Issues**: Search existing [issues](https://github.com/wowtalon/xsoc/issues)
- **Discussions**: Join [discussions](https://github.com/wowtalon/xsoc/discussions)
- **Discord**: Join our Discord server (if available)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to XSOC! 🚀