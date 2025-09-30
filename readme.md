# DC Logger

A comprehensive structured logging system for Domo applications with support for multiple output handlers, correlation tracking, and cloud integrations.

## Features

- **Multiple Output Handlers**: Console, file, and cloud integrations (Datadog, AWS, GCP, Azure)
- **Structured Logging**: JSON-formatted logs with rich contextual information
- **Correlation Tracking**: Distributed tracing with trace IDs, span IDs, and request IDs
- **Async & Sync Support**: Works in both async and synchronous environments
- **Decorator-Based Logging**: Automatic function call logging with `@log_function_call`
- **Multi-Tenant Support**: Track users, sessions, tenants, and organizations
- **HTTP Details**: Capture request/response information automatically
- **Entity Tracking**: Log operations on datasets, users, cards, etc.
- **Flexible Configuration**: Simple factory functions or custom configs
- **SOLID Principles**: Clean, maintainable, extensible architecture

## Installation

```bash
pip install -e .
```

## Quick Start

### Basic Console Logging

```python
import asyncio
from dc_logger import get_logger, LogLevel

async def main():
    logger = get_logger("myapp")
    
    await logger.info("Application started")
    await logger.debug("Debug information")
    await logger.error("Something went wrong", extra={"error_code": 500})
    
    await logger.close()

asyncio.run(main())
```

### Console + File Logging

```python
from dc_logger import DomoLogger, create_console_file_config, LogLevel

config = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO,
    pretty_print=True
)
logger = DomoLogger(config, "myapp")

await logger.info("Logging to both console and file")
```

### Datadog Integration

```python
from dc_logger import DomoLogger, create_console_datadog_config

config = create_console_datadog_config(
    datadog_api_key="your-api-key",
    datadog_service="myapp",
    datadog_env="production"
)
logger = DomoLogger(config, "myapp")

await logger.info("Sent to both console and Datadog")
```

### Using the Decorator

```python
from dc_logger import log_function_call, LogLevel

@log_function_call(
    action_name="fetch_user_data",
    include_params=True,
    log_level=LogLevel.INFO
)
async def fetch_user_data(user_id: str, auth=None):
    # Your code here
    return data
```

### Structured Logging with Context

```python
from dc_logger import get_logger, Entity, HTTPDetails

logger = get_logger("myapp")

entity = Entity(type="dataset", id="abc123", name="Sales Data")
http_details = HTTPDetails(method="GET", url="/api/data", status_code=200)

await logger.info(
    "Data fetched successfully",
    action="fetch_data",
    entity=entity,
    http_details=http_details,
    duration_ms=250,
    extra={"rows": 1000}
)
```

## Project Structure

```
dc_logger/
├── client/              # Core data models and utilities
├── configs/             # Configuration classes
├── handlers/            # Log output handlers
│   └── cloud/          # Cloud platform integrations
├── logger.py           # Main DomoLogger class
├── decorators.py       # Decorator for automatic logging
├── utils.py            # Utility functions
└── readme.md           # This file
```

See [architecture.md](architecture.md) for detailed documentation.

## Configuration

### Environment Variables

For Azure Log Analytics (default):
```bash
AZURE_WORKSPACE_ID=workspace-id
AZURE_SHARED_KEY=shared-key
LOG_LEVEL=INFO
LOG_BATCH_SIZE=100
LOG_FLUSH_INTERVAL=30
```

### Factory Functions

- `create_console_config()` - Simple console logging
- `create_file_config()` - File logging
- `create_console_file_config()` - Console + file
- `create_console_datadog_config()` - Console + Datadog
- `create_console_file_datadog_config()` - Console + file + Datadog
- `create_file_datadog_config()` - File + Datadog

## Log Levels

- `DEBUG` - Detailed information for debugging
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors

## Best Practices

1. Always `await` async methods (log, flush, close)
2. Use factory functions for common configurations
3. Provide context in log calls (entity, action, etc.)
4. Use structured logging with extra fields
5. Close logger properly on application shutdown
6. Use correlation IDs for distributed tracing
7. Sanitize sensitive data before logging

## Development Guidelines

### Code Style

- Classes: `PascalCase` (e.g., `DomoLogger`, `ConsoleHandler`)
- Functions: `snake_case` (e.g., `get_logger`, `create_console_config`)
- Follow SOLID principles
- Write clean, concise, readable code
- Follow best practices for the technology stack

### Project Organization

- Split classes into separate files unless closely related
- Use classes with methods that call route functions
- Keep files focused and maintainable
- Update exports in `__init__.py` files

## Contributing

1. Follow the existing code structure and patterns
2. Respect SOLID principles
3. Use correct naming conventions
4. Write concise, readable code
5. Add tests for new functionality
6. Update documentation

## License


## Support

For issues, questions, or contributions, please [open an issue](your-repo-url).