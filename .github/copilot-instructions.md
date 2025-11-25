# DC Logger - GitHub Copilot Instructions

## About This Library

DC Logger is an async-first structured logging library for Python with support for:
- Multiple output handlers (console, file, cloud)
- Distributed tracing with correlation IDs
- Decorator-based automatic function logging
- Cloud integrations (Datadog, AWS CloudWatch, GCP, Azure)

## Code Style and Conventions

### Async Patterns
- All logging methods are async and must be awaited
- Always close the logger with `await logger.close()` on shutdown
- Use `async def` for functions that perform logging

### Imports
```python
# Preferred import style
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel
from dc_logger import LogEntity, HTTPDetails, log_call
```

### Logging Best Practices
- Use structured context parameters instead of string formatting
- Include `entity` for operations on specific objects
- Add `duration_ms` for performance-sensitive operations
- Use `extra={}` dict for additional metadata
- Apply `@log_call` decorator for automatic function logging

### Configuration
- Use factory functions like `create_console_file_config()` for common setups
- Set `pretty_print=True` only in development
- Use `LogLevel.DEBUG` for development, `LogLevel.INFO` for production

## Testing
- Run tests with `python -m pytest tests/`
- Install dev dependencies: `pip install -e .[dev]`

## Documentation
- See `.ai/context.md` for quick reference
- See `USAGE.md` for comprehensive examples
- See `API_REFERENCE.md` for complete API docs
