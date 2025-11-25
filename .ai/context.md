# DC Logger - AI Agent Context

> Quick reference guide for AI agents integrating with the dc_logger library.

## Library Purpose

DC Logger is a structured logging library for Python applications with:
- **Async-first design** - All logging methods are async
- **Multiple output handlers** - Console, file, and cloud (Datadog, AWS, GCP, Azure)
- **Distributed tracing** - Built-in correlation tracking with trace/span IDs
- **Structured logging** - JSON-based logs with entities, HTTP details, and context
- **Decorator-based logging** - Automatic function logging with `@log_call`

## Quick Integration

### Minimal Setup

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

async def main():
    config = ConsoleLogConfig(level=LogLevel.INFO)
    logger = DCLogger(config, "my_app")
    
    await logger.info("Hello from dc_logger")
    await logger.close()

asyncio.run(main())
```

### Using Global Logger

```python
from dc_logger import get_logger

logger = get_logger("my_app")
# Logger is auto-configured with console output
```

### Decorator Usage

```python
from dc_logger import log_call

@log_call(action_name="process", include_params=True)
async def process_data(data_id: str):
    return {"id": data_id, "status": "done"}
```

## Core Components

| Component | Import | Purpose |
|-----------|--------|---------|
| `DCLogger` | `from dc_logger import DCLogger` | Main logger class |
| `ConsoleLogConfig` | `from dc_logger import ConsoleLogConfig` | Console configuration |
| `LogLevel` | `from dc_logger import LogLevel` | Log levels enum |
| `LogEntity` | `from dc_logger import LogEntity` | Entity context |
| `HTTPDetails` | `from dc_logger import HTTPDetails` | HTTP request details |
| `log_call` | `from dc_logger import log_call` | Function decorator |
| `get_logger` | `from dc_logger import get_logger` | Global logger access |
| `correlation_manager` | `from dc_logger import correlation_manager` | Trace management |

## Common Patterns

### Pattern 1: Structured Logging

```python
await logger.info(
    "Data processed",
    entity=LogEntity(type="dataset", id="ds123"),
    action="process_data",
    duration_ms=150,
    extra={"rows": 1000}
)
```

### Pattern 2: Error Logging

```python
try:
    result = await process()
except Exception as e:
    await logger.error(
        f"Processing failed: {e}",
        extra={"error_type": type(e).__name__}
    )
    raise
```

### Pattern 3: API Request Logging

```python
await logger.info(
    "API call completed",
    http_details=HTTPDetails(
        method="POST",
        url="/api/data",
        status_code=200
    ),
    duration_ms=250
)
```

### Pattern 4: Multi-Handler Setup

```python
from dc_logger import create_console_file_config

config = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO
)
logger = DCLogger(config, "my_app")
```

## Log Levels

| Level | When to Use |
|-------|-------------|
| `DEBUG` | Detailed debugging info |
| `INFO` | General operations |
| `WARNING` | Potential issues |
| `ERROR` | Operation failures |
| `CRITICAL` | System-level failures |

## API Summary

### DCLogger Methods

```python
# Logging
await logger.debug(message, **context)
await logger.info(message, **context)
await logger.warning(message, **context)
await logger.error(message, **context)
await logger.critical(message, **context)
await logger.log(LogLevel.INFO, message, **context)

# Lifecycle
await logger.flush()  # Flush buffered logs
await logger.close()  # Cleanup resources

# Correlation
logger.start_request()  # Start trace context
logger.end_request()    # End trace context
```

### Context Parameters

All logging methods accept these context kwargs:

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `str` | Action being performed |
| `entity` | `LogEntity` | Entity being operated on |
| `user` | `str` | User identifier |
| `duration_ms` | `int` | Operation duration |
| `http_details` | `HTTPDetails` | HTTP request info |
| `multi_tenant` | `MultiTenant` | Tenant context |
| `extra` | `dict` | Additional metadata |
| `color` | `str` | Console output color |

## Configuration Options

### ConsoleLogConfig

```python
ConsoleLogConfig(
    level=LogLevel.INFO,      # Minimum level
    format="json",            # "json" or "text"
    pretty_print=False,       # Pretty JSON
    batch_size=100,           # Buffer size
    flush_interval=30         # Auto-flush seconds
)
```

## Best Practices

1. **Always close the logger** - Call `await logger.close()` on shutdown
2. **Use structured context** - Use entity/action/extra instead of string formatting
3. **Leverage decorators** - Use `@log_call` for automatic function logging
4. **Set appropriate levels** - DEBUG for dev, INFO/WARNING for production
5. **Include durations** - Add `duration_ms` for performance tracking

## Files to Know

| File | Contains |
|------|----------|
| `src/dc_logger/__init__.py` | All public exports |
| `src/dc_logger/logger.py` | DCLogger class |
| `src/dc_logger/decorators.py` | @log_call decorator |
| `src/dc_logger/client/models.py` | Data models |
| `src/dc_logger/configs/*.py` | Configuration classes |
| `src/dc_logger/handlers/*.py` | Output handlers |

## Error Handling

```python
from dc_logger.client.exceptions import (
    LoggingError,      # Base exception
    LogConfigError,    # Configuration errors
    LogHandlerError,   # Handler errors
    LogWriteError,     # Write failures
    LogFlushError      # Flush failures
)
```

## When to Use What

| Use Case | Solution |
|----------|----------|
| Simple console logging | `ConsoleLogConfig` |
| Console + file | `create_console_file_config()` |
| Cloud integration | `DatadogLogConfig` or `create_console_datadog_config()` |
| Function logging | `@log_call` decorator |
| Distributed tracing | `correlation_manager` |
| Multi-tenant apps | `MultiTenant` context |

## See Also

- [USAGE.md](../USAGE.md) - Comprehensive usage guide
- [API_REFERENCE.md](../API_REFERENCE.md) - Full API documentation
- [examples/](../examples/) - Working code examples
