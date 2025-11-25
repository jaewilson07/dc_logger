---
applyTo: "**/*.py"
---

# DC Logger - Usage Instructions and Best Practices

## Library Overview

DC Logger is an async-first structured logging library for Python applications. It provides:
- Async logging methods for non-blocking I/O
- Multiple output handlers (console, file, cloud)
- Distributed tracing with correlation IDs
- Decorator-based automatic function logging
- Cloud integrations (Datadog, AWS, GCP, Azure)

## Quick Start

### Minimal Setup

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

async def main():
    config = ConsoleLogConfig(level=LogLevel.INFO)
    logger = DCLogger(config, "my_app")
    await logger.info("Hello, dc_logger!")
    await logger.close()

asyncio.run(main())
```

### Using Global Logger

```python
from dc_logger import get_logger

logger = get_logger("my_app")
# Use in async context
await logger.info("Using global logger")
```

## Core Imports

```python
# Essential imports
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

# With entities and context
from dc_logger import LogEntity, HTTPDetails, MultiTenant

# Decorators
from dc_logger import log_call, LogDecoratorConfig

# Correlation tracking
from dc_logger import correlation_manager

# Factory functions
from dc_logger import (
    create_console_config,
    create_file_config,
    create_console_file_config,
    create_console_datadog_config,
)
```

## Logging Best Practices

### 1. Always Close the Logger

```python
async def main():
    logger = DCLogger(config, "my_app")
    try:
        await run_application()
    finally:
        await logger.close()  # Always close to flush logs
```

### 2. Use Structured Context Instead of String Formatting

```python
# ❌ Bad: String concatenation
await logger.info(f"User {user_id} logged in from {ip}")

# ✅ Good: Structured context
await logger.info(
    "User logged in",
    user=user_id,
    extra={"ip": ip}
)
```

### 3. Use Entities for Consistent Logging

```python
from dc_logger import LogEntity

entity = LogEntity(
    type="dataset",
    id="ds_123",
    name="Sales Data"
)

await logger.info("Dataset processed", entity=entity)
```

### 4. Use Decorators for Function Logging

```python
from dc_logger import log_call

@log_call(action_name="process_order", include_params=True)
async def process_order(order_id: str, customer_id: str):
    # Automatically logs entry, exit, duration, and errors
    return {"status": "completed"}
```

### 5. Include Duration for Performance Tracking

```python
import time

start = time.time()
result = await operation()
duration_ms = int((time.time() - start) * 1000)

await logger.info(
    "Operation completed",
    action="operation_name",
    duration_ms=duration_ms
)
```

### 6. Sanitize Sensitive Data

```python
@log_call(
    sensitive_params=["password", "api_key", "token"]
)
async def authenticate(username: str, password: str):
    # password will be logged as "***"
    pass
```

## Log Levels Guide

| Level | When to Use |
|-------|-------------|
| `DEBUG` | Detailed debugging info for development |
| `INFO` | Normal operations, general events |
| `WARNING` | Potential issues that may need attention |
| `ERROR` | Errors that need to be addressed |
| `CRITICAL` | Critical failures requiring immediate action |

## Configuration Patterns

### Development Configuration

```python
config = ConsoleLogConfig(
    level=LogLevel.DEBUG,
    pretty_print=True
)
```

### Production Configuration

```python
config = ConsoleLogConfig(
    level=LogLevel.INFO,
    format="json",
    pretty_print=False
)
```

### Console + File Logging

```python
from dc_logger import create_console_file_config

config = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO
)
```

### With Datadog

```python
from dc_logger import create_console_datadog_config

config = create_console_datadog_config(
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production"
)
```

## Context Parameters

All logging methods accept these context parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `str` | Action being performed |
| `entity` | `LogEntity` | Entity being operated on |
| `user` | `str` | User identifier |
| `duration_ms` | `int` | Operation duration in milliseconds |
| `http_details` | `HTTPDetails` | HTTP request/response details |
| `multi_tenant` | `MultiTenant` | Multi-tenant context |
| `extra` | `dict` | Additional metadata |
| `color` | `str` | Console output color |

## Error Handling Pattern

```python
entity = LogEntity(type="data", id=data_id)

try:
    await logger.info("Starting operation", entity=entity, action="process")
    result = await process_data(data_id)
    await logger.info("Operation completed", entity=entity, duration_ms=elapsed)
except Exception as e:
    await logger.error(
        f"Operation failed: {e}",
        entity=entity,
        extra={"error_type": type(e).__name__}
    )
    raise
```

## HTTP Request Logging

```python
from dc_logger import HTTPDetails

http = HTTPDetails(
    method="POST",
    url="/api/v1/data",
    status_code=201,
    response_size=1024
)

await logger.info("API request completed", http_details=http, duration_ms=250)
```

## Distributed Tracing

```python
from dc_logger import correlation_manager

# Start a new trace
request_id = correlation_manager.start_request()

# Get current correlation context
context = correlation_manager.get_current_context()
trace_id = context["trace_id"]

# Logs automatically include trace_id and span_id
await logger.info("Processing request")
```

## Common Anti-Patterns to Avoid

1. **Not closing the logger** - Always call `await logger.close()`
2. **Logging in tight loops** - Log summaries, not every iteration
3. **Missing await** - All logging methods are async, always await them
4. **Over-logging** - Use appropriate log levels, don't log everything at DEBUG
5. **Logging secrets** - Use `sensitive_params` in decorators

## File Structure Reference

| File | Purpose |
|------|---------|
| `src/dc_logger/__init__.py` | All public exports |
| `src/dc_logger/logger.py` | DCLogger main class |
| `src/dc_logger/decorators.py` | @log_call decorator |
| `src/dc_logger/client/models.py` | LogEntity, HTTPDetails, etc. |
| `src/dc_logger/client/enums.py` | LogLevel enum |
| `src/dc_logger/configs/*.py` | Configuration classes |
| `src/dc_logger/handlers/*.py` | Output handlers |

## Additional Resources

- [USAGE.md](../../USAGE.md) - Comprehensive usage guide
- [API_REFERENCE.md](../../API_REFERENCE.md) - Complete API documentation
- [examples/](../../examples/) - Working example scripts
- [.ai/context.md](../../.ai/context.md) - AI agent quick reference
