# DC Logger Usage Guide

A comprehensive guide to using the dc_logger library for structured logging with support for cloud providers, multi-tenancy, and distributed tracing.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Logging](#basic-logging)
- [Configuration Options](#configuration-options)
- [Using Decorators](#using-decorators)
- [Correlation and Tracing](#correlation-and-tracing)
- [Multi-Handler Setup](#multi-handler-setup)
- [Cloud Integrations](#cloud-integrations)
- [Common Patterns](#common-patterns)

## Installation

```bash
pip install dc_logger

# With Datadog support
pip install dc_logger[datadog]

# With all extras
pip install dc_logger[all]
```

## Quick Start

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

async def main():
    # Create a simple console logger
    config = ConsoleLogConfig(level=LogLevel.INFO)
    logger = DCLogger(config, app_name="my_app")
    
    # Log messages at different levels
    await logger.info("Application started")
    await logger.warning("This is a warning")
    await logger.error("Something went wrong")
    
    # Always close the logger when done
    await logger.close()

asyncio.run(main())
```

## Basic Logging

### Creating a Logger

```python
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

# Console logger with default settings
config = ConsoleLogConfig(level=LogLevel.INFO)
logger = DCLogger(config, app_name="my_app")

# Console logger with pretty printing (for development)
config = ConsoleLogConfig(
    level=LogLevel.DEBUG,
    pretty_print=True
)
logger = DCLogger(config, app_name="my_app")
```

### Log Levels

DC Logger supports standard log levels in order of increasing severity:

```python
from dc_logger import LogLevel

# Available levels
LogLevel.DEBUG      # Detailed debugging information
LogLevel.INFO       # General informational messages
LogLevel.WARNING    # Warning messages for potential issues
LogLevel.ERROR      # Error messages for failures
LogLevel.CRITICAL   # Critical errors requiring immediate attention
```

### Logging with Context

```python
from dc_logger import LogEntity

# Log with entity information
entity = LogEntity(
    type="dataset",
    id="ds_12345",
    name="Sales Data"
)

await logger.info(
    "Dataset processed successfully",
    entity=entity,
    action="process_dataset",
    duration_ms=1500
)

# Log with extra metadata
await logger.info(
    "User logged in",
    user="user@example.com",
    extra={
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0"
    }
)
```

### HTTP Details

```python
from dc_logger import HTTPDetails

http_details = HTTPDetails(
    method="GET",
    url="/api/v1/datasets/12345",
    status_code=200,
    response_size=4096
)

await logger.info(
    "API request completed",
    http_details=http_details,
    duration_ms=250
)
```

## Configuration Options

### ConsoleLogConfig

```python
from dc_logger import ConsoleLogConfig, LogLevel

config = ConsoleLogConfig(
    level=LogLevel.INFO,           # Minimum log level
    format="json",                 # Output format: "json" or "text"
    pretty_print=False,            # Pretty print JSON output
    batch_size=100,                # Logs to buffer before flush
    flush_interval=30,             # Seconds between auto-flushes
    correlation_enabled=True,      # Enable correlation tracking
    include_traceback=True         # Include stack traces for errors
)
```

### MultiHandlerLogConfig

```python
from dc_logger import (
    MultiHandlerLogConfig,
    HandlerConfig,
    LogLevel
)

config = MultiHandlerLogConfig(
    level=LogLevel.INFO,
    handlers=[
        HandlerConfig(
            handler_type="console",
            config={"format": "text", "pretty_print": True}
        ),
        HandlerConfig(
            handler_type="file",
            config={"destination": "logs/app.log"}
        )
    ]
)
```

### Factory Functions

For convenience, use the built-in factory functions:

```python
from dc_logger import (
    create_console_config,
    create_file_config,
    create_console_file_config,
    create_console_datadog_config,
    LogLevel
)

# Simple console configuration
config = create_console_config(level=LogLevel.DEBUG)

# File-only configuration
config = create_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO
)

# Console + File
config = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO,
    pretty_print=True
)

# Console + Datadog
config = create_console_datadog_config(
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production"
)
```

## Using Decorators

### Basic Decorator Usage

```python
from dc_logger import log_call, LogLevel

@log_call()
async def process_data(data_id: str):
    """Automatically logs function entry and exit."""
    result = await fetch_data(data_id)
    return result

# With custom options
@log_call(
    action_name="process_order",
    log_level=LogLevel.DEBUG,
    include_params=True
)
async def process_order(order_id: str, customer_id: str):
    """Logs with custom action name and includes parameters."""
    return {"order_id": order_id, "status": "processed"}
```

### LogDecoratorConfig

For advanced customization:

```python
from dc_logger import log_call, LogDecoratorConfig

config = LogDecoratorConfig(
    action_name="custom_action",
    level_name="api_call",
    log_level=LogLevel.INFO,
    include_params=True,
    sensitive_params=["password", "api_key", "token"],
    color="green"
)

@log_call(config=config)
async def my_function(user_id: str, password: str):
    """Password will be sanitized in logs."""
    pass
```

### Logger Injection

```python
from dc_logger import log_call, get_logger

# Using logger getter for late binding
@log_call(logger_getter=get_logger)
async def my_function():
    pass

# Using direct logger instance
my_logger = get_logger("my_app")

@log_call(logger=my_logger)
async def another_function():
    pass
```

## Correlation and Tracing

### Using CorrelationManager

```python
from dc_logger import correlation_manager

# Start a new request context
request_id = correlation_manager.start_request()

# Start with parent trace (for distributed tracing)
request_id = correlation_manager.start_request(
    parent_trace_id="abc123"
)

# Get current correlation context
context = correlation_manager.get_current_context()
print(f"Trace ID: {context['trace_id']}")
print(f"Span ID: {context['span_id']}")
```

### Request Lifecycle

```python
from dc_logger import DCLogger, ConsoleLogConfig

logger = DCLogger(ConsoleLogConfig(), "my_app")

# Start a request
trace_id = logger.start_request()

try:
    await logger.info("Processing request")
    # Your code here
finally:
    logger.end_request()
```

### Multi-Tenant Context

```python
from dc_logger import MultiTenant

tenant = MultiTenant(
    user_id="user123",
    tenant_id="tenant456",
    organization_id="org789",
    session_id="session_abc"
)

await logger.info(
    "Processing tenant request",
    multi_tenant=tenant
)
```

## Multi-Handler Setup

### Console + File

```python
from dc_logger import DCLogger, create_console_file_config

config = create_console_file_config(
    file_path="logs/application.log",
    level=LogLevel.INFO,
    pretty_print=True
)

logger = DCLogger(config, "my_app")
```

### Console + Cloud

```python
from dc_logger import DCLogger, create_console_datadog_config

config = create_console_datadog_config(
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production"
)

logger = DCLogger(config, "my_app")
```

### Custom Multi-Handler

```python
from dc_logger import (
    DCLogger,
    MultiHandlerLogConfig,
    HandlerConfig,
    LogLevel
)

config = MultiHandlerLogConfig(
    level=LogLevel.INFO,
    handlers=[
        HandlerConfig(
            handler_type="console",
            config={"pretty_print": True}
        ),
        HandlerConfig(
            handler_type="file",
            config={"destination": "logs/app.log"}
        ),
        HandlerConfig(
            handler_type="cloud",
            cloud_config={
                "cloud_provider": "datadog",
                "api_key": "your-key",
                "service": "my-service"
            }
        )
    ]
)

logger = DCLogger(config, "my_app")
```

## Cloud Integrations

### Datadog

```python
from dc_logger import DCLogger, DatadogLogConfig

config = DatadogLogConfig(
    api_key="your-datadog-api-key",
    service="my-service",
    env="production",
    level=LogLevel.INFO
)

logger = DCLogger(config, "my_app")
```

### AWS CloudWatch (Coming Soon)

```python
from dc_logger import DCLogger, AWSCloudWatchLogConfig

config = AWSCloudWatchLogConfig(
    log_group="my-log-group",
    log_stream="my-log-stream",
    region="us-east-1",
    level=LogLevel.INFO
)

logger = DCLogger(config, "my_app")
```

### GCP Logging (Coming Soon)

```python
from dc_logger import DCLogger, GCPLoggingConfig

config = GCPLoggingConfig(
    project_id="my-project",
    log_name="my-log",
    level=LogLevel.INFO
)

logger = DCLogger(config, "my_app")
```

## Common Patterns

### Global Logger Pattern

```python
from dc_logger import get_logger, set_global_logger, DCLogger, ConsoleLogConfig

# Option 1: Use default global logger
logger = get_logger("my_app")

# Option 2: Set custom global logger
custom_logger = DCLogger(
    ConsoleLogConfig(level=LogLevel.DEBUG),
    "my_app"
)
set_global_logger(custom_logger)

# Now get_logger returns the custom logger
logger = get_logger()
```

### Structured Error Logging

```python
async def process_data(data_id: str):
    try:
        result = await fetch_data(data_id)
        await logger.info(
            "Data processed successfully",
            action="process_data",
            entity=LogEntity(type="data", id=data_id),
            duration_ms=elapsed_ms
        )
        return result
    except Exception as e:
        await logger.error(
            f"Failed to process data: {str(e)}",
            action="process_data",
            entity=LogEntity(type="data", id=data_id),
            extra={
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )
        raise
```

### API Request Logging

```python
from dc_logger import log_call, HTTPDetails

@log_call(action_name="api_request")
async def make_api_request(url: str, method: str = "GET"):
    start = time.time()
    response = await http_client.request(method, url)
    
    await logger.info(
        "API request completed",
        http_details=HTTPDetails(
            method=method,
            url=url,
            status_code=response.status_code,
            response_size=len(response.content)
        ),
        duration_ms=int((time.time() - start) * 1000)
    )
    
    return response
```

### Application Lifecycle

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

async def main():
    # Initialize logger
    config = ConsoleLogConfig(level=LogLevel.INFO)
    logger = DCLogger(config, "my_app")
    
    try:
        await logger.info("Application starting")
        
        # Your application code here
        await run_application()
        
        await logger.info("Application completed successfully")
    except Exception as e:
        await logger.critical(f"Application failed: {e}")
        raise
    finally:
        # Always close the logger
        await logger.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Console Color Output

```python
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

config = ConsoleLogConfig(level=LogLevel.DEBUG, format="text")
logger = DCLogger(config, "my_app")

# Default colors based on log level
await logger.debug("Debug - green")
await logger.info("Info - green")
await logger.warning("Warning - yellow")
await logger.error("Error - red")

# Custom colors
await logger.info("Custom blue message", color="blue")
await logger.info("Bold green", color="bold_green")
```

## Best Practices

1. **Always close the logger** when your application exits
2. **Use structured logging** with entities and context instead of string interpolation
3. **Leverage the decorator** for automatic function logging
4. **Set appropriate log levels** based on environment (DEBUG for dev, INFO/WARNING for prod)
5. **Use correlation IDs** for distributed tracing across services
6. **Sanitize sensitive data** using the `sensitive_params` option in decorators
7. **Batch logs appropriately** to reduce I/O overhead in high-throughput scenarios
8. **Include HTTP details** for API calls to aid debugging
9. **Use multi-tenant context** when building multi-tenant applications

## See Also

- [API Reference](./API_REFERENCE.md) - Complete API documentation
- [Examples](./examples/) - Working example scripts
- [Architecture](./documentation/architecture.md) - Design and architecture details
- [AI Agent Guide](./.ai/context.md) - Quick reference for AI agents
