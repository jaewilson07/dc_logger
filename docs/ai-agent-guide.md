# DC Logger - AI Agent Integration Guide

A guide specifically optimized for AI agents integrating with the dc_logger library.

## Quick Facts

| Aspect | Detail |
|--------|--------|
| **Language** | Python 3.8+ |
| **Type** | Async-first structured logging |
| **Main Class** | `DCLogger` |
| **Config Class** | `ConsoleLogConfig`, `DatadogLogConfig`, etc. |
| **Decorator** | `@log_call` |
| **Package** | `dc_logger` |

## Import Patterns

```python
# Most common imports
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

# With entities
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel, LogEntity

# With decorators
from dc_logger import log_call, LogDecoratorConfig

# With HTTP details
from dc_logger import HTTPDetails

# With correlation
from dc_logger import correlation_manager, Correlation

# Full import
from dc_logger import (
    DCLogger,
    ConsoleLogConfig,
    LogLevel,
    LogEntity,
    HTTPDetails,
    Correlation,
    MultiTenant,
    log_call,
    get_logger,
    set_global_logger,
    correlation_manager,
)
```

## Minimal Working Example

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

async def main():
    config = ConsoleLogConfig(level=LogLevel.INFO)
    logger = DCLogger(config, "my_app")
    await logger.info("Hello")
    await logger.close()

asyncio.run(main())
```

## Method Signatures

### DCLogger Constructor

```python
DCLogger(config: LogConfig, app_name: str)
```

### Logging Methods

```python
await logger.debug(message: str, **context) -> bool
await logger.info(message: str, **context) -> bool
await logger.warning(message: str, **context) -> bool
await logger.error(message: str, **context) -> bool
await logger.critical(message: str, **context) -> bool
await logger.log(level: LogLevel, message: str, **context) -> bool
```

### Context Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `str` | Action name |
| `entity` | `LogEntity` | Entity being operated on |
| `user` | `str` | User identifier |
| `duration_ms` | `int` | Duration in milliseconds |
| `http_details` | `HTTPDetails` | HTTP request/response |
| `multi_tenant` | `MultiTenant` | Tenant context |
| `extra` | `dict` | Additional metadata |
| `color` | `str` | Console color |

### Lifecycle Methods

```python
await logger.flush() -> bool    # Flush buffered logs
await logger.close() -> None    # Cleanup and close
logger.start_request() -> str   # Start trace context
logger.end_request() -> None    # End trace context
```

## Common Configuration Patterns

### Development

```python
config = ConsoleLogConfig(level=LogLevel.DEBUG, pretty_print=True)
```

### Production Console

```python
config = ConsoleLogConfig(level=LogLevel.INFO)
```

### Console + File

```python
from dc_logger import create_console_file_config
config = create_console_file_config(file_path="logs/app.log", level=LogLevel.INFO)
```

### Console + Datadog

```python
from dc_logger import create_console_datadog_config
config = create_console_datadog_config(
    datadog_api_key="key",
    datadog_service="service",
    datadog_env="production"
)
```

## Decorator Usage

### Basic

```python
from dc_logger import log_call

@log_call()
async def my_function():
    pass
```

### With Options

```python
@log_call(
    action_name="custom_action",
    log_level=LogLevel.DEBUG,
    include_params=True,
    sensitive_params=["password", "token"]
)
async def my_function(user_id: str, password: str):
    pass
```

## Entity Creation

```python
entity = LogEntity(
    type="dataset",      # Required: entity type
    id="ds_123",         # Optional: identifier
    name="My Dataset",   # Optional: human name
    additional_info={}   # Optional: extra metadata
)
```

## HTTP Details

```python
http = HTTPDetails(
    method="POST",
    url="/api/data",
    status_code=201,
    response_size=1024
)

await logger.info("API call", http_details=http)
```

## Error Handling

```python
try:
    result = await operation()
except Exception as e:
    await logger.error(
        f"Failed: {e}",
        extra={"error_type": type(e).__name__}
    )
    raise
```

## Global Logger

```python
from dc_logger import get_logger, set_global_logger

# Get default
logger = get_logger("my_app")

# Set custom
custom_logger = DCLogger(config, "my_app")
set_global_logger(custom_logger)
```

## File Structure

```
dc_logger/
├── __init__.py          # All exports
├── logger.py            # DCLogger class
├── decorators.py        # @log_call
├── client/
│   ├── models.py        # LogEntity, HTTPDetails, etc.
│   ├── enums.py         # LogLevel
│   └── exceptions.py    # Error types
├── configs/
│   ├── console.py       # ConsoleLogConfig
│   ├── cloud.py         # DatadogLogConfig, etc.
│   └── factory.py       # Factory functions
└── handlers/
    ├── console.py       # ConsoleHandler
    ├── file.py          # FileHandler
    └── cloud/           # Cloud handlers
```

## Common Mistakes to Avoid

1. **Missing await** - All logging methods are async
2. **Not closing logger** - Always call `await logger.close()`
3. **Using sync in async** - Use async logging in async code
4. **Forgetting to import** - Import LogLevel, not just DCLogger

## Decision Tree

```
Need logging?
├── Simple console → ConsoleLogConfig
├── Console + file → create_console_file_config()
├── Cloud logging → DatadogLogConfig or create_console_datadog_config()
├── Multiple outputs → MultiHandlerLogConfig
└── Automatic function logging → @log_call decorator
```

## Log Level Selection

| Situation | Level |
|-----------|-------|
| Debugging info | `DEBUG` |
| Normal operations | `INFO` |
| Potential issues | `WARNING` |
| Errors | `ERROR` |
| Critical failures | `CRITICAL` |

## Performance Notes

- Logs are buffered (default: 100 logs before flush)
- Auto-flush every 30 seconds
- Call `flush()` for immediate output
- Use higher log levels in production

## Related Files

- [USAGE.md](../USAGE.md) - Comprehensive examples
- [API_REFERENCE.md](../API_REFERENCE.md) - Complete API docs
- [.ai/context.md](../.ai/context.md) - Quick reference
- [.ai/examples.yaml](../.ai/examples.yaml) - Structured examples
