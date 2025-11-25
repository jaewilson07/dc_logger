# DC Logger Configuration Guide

Complete guide to configuring dc_logger for different use cases.

## Table of Contents

- [Configuration Classes](#configuration-classes)
- [Console Configuration](#console-configuration)
- [File Configuration](#file-configuration)
- [Multi-Handler Configuration](#multi-handler-configuration)
- [Cloud Configurations](#cloud-configurations)
- [Factory Functions](#factory-functions)
- [Common Settings](#common-settings)
- [Environment-Specific Configurations](#environment-specific-configurations)

## Configuration Classes

DC Logger uses configuration classes to define logging behavior:

| Class | Purpose |
|-------|---------|
| `ConsoleLogConfig` | Console/stdout output |
| `DatadogLogConfig` | Datadog cloud logging |
| `AWSCloudWatchLogConfig` | AWS CloudWatch |
| `GCPLoggingConfig` | Google Cloud Logging |
| `AzureLogAnalyticsConfig` | Azure Log Analytics |
| `MultiHandlerLogConfig` | Multiple handlers |

## Console Configuration

### Basic Console Setup

```python
from dc_logger import ConsoleLogConfig, LogLevel

config = ConsoleLogConfig(
    level=LogLevel.INFO
)
```

### All Console Options

```python
config = ConsoleLogConfig(
    # Log level filtering
    level=LogLevel.INFO,           # Minimum level to log
    
    # Output format
    format="json",                 # "json" or "text"
    pretty_print=False,            # Pretty-print JSON output
    
    # Buffering
    batch_size=100,                # Logs to buffer before flush
    flush_interval=30,             # Seconds between auto-flushes
    max_buffer_size=1000,          # Maximum buffer size
    
    # Features
    correlation_enabled=True,      # Enable correlation tracking
    include_traceback=True         # Include stack traces for errors
)
```

### Development vs Production

```python
# Development: Pretty output, all levels
dev_config = ConsoleLogConfig(
    level=LogLevel.DEBUG,
    pretty_print=True
)

# Production: Compact JSON, INFO and above
prod_config = ConsoleLogConfig(
    level=LogLevel.INFO,
    format="json",
    pretty_print=False
)
```

## File Configuration

### Using Factory Function

```python
from dc_logger import create_file_config, LogLevel

config = create_file_config(
    file_path="logs/application.log",
    level=LogLevel.INFO
)
```

### Combined Console + File

```python
from dc_logger import create_console_file_config

config = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO,
    pretty_print=True
)
```

### File Handler Notes

- Directory is created automatically if it doesn't exist
- Logs are appended to existing files
- Consider log rotation for production (not built-in)

## Multi-Handler Configuration

### Basic Multi-Handler

```python
from dc_logger import MultiHandlerLogConfig
from dc_logger.configs import HandlerConfig

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
        )
    ]
)
```

### Handler Types

| Type | Description |
|------|-------------|
| `"console"` | Standard output |
| `"file"` | File output |
| `"cloud"` | Cloud provider (requires `cloud_config`) |

### Cloud Handler in Multi-Handler

```python
config = MultiHandlerLogConfig(
    level=LogLevel.INFO,
    handlers=[
        HandlerConfig(
            handler_type="console",
            config={}
        ),
        HandlerConfig(
            handler_type="cloud",
            config={},
            cloud_config={
                "cloud_provider": "datadog",
                "api_key": "your-api-key",
                "service": "my-service",
                "env": "production"
            }
        )
    ]
)
```

## Cloud Configurations

### Datadog

```python
from dc_logger import DatadogLogConfig, LogLevel

config = DatadogLogConfig(
    api_key="your-datadog-api-key",
    service="my-service",
    env="production",
    level=LogLevel.INFO,
    
    # Optional
    source="python",
    hostname="server-01",
    tags=["team:backend", "version:1.0"]
)
```

### Console + Datadog

```python
from dc_logger import create_console_datadog_config

config = create_console_datadog_config(
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production",
    level=LogLevel.INFO
)
```

### AWS CloudWatch (Placeholder)

```python
from dc_logger import AWSCloudWatchLogConfig

config = AWSCloudWatchLogConfig(
    log_group="my-app",
    log_stream="production",
    region="us-east-1",
    level=LogLevel.INFO
)
```

### GCP Logging (Placeholder)

```python
from dc_logger import GCPLoggingConfig

config = GCPLoggingConfig(
    project_id="my-gcp-project",
    log_name="application",
    level=LogLevel.INFO
)
```

### Azure Log Analytics (Placeholder)

```python
from dc_logger import AzureLogAnalyticsConfig

config = AzureLogAnalyticsConfig(
    workspace_id="your-workspace-id",
    shared_key="your-shared-key",
    log_type="ApplicationLog",
    level=LogLevel.INFO
)
```

## Factory Functions

Quick configuration creation:

| Function | Output |
|----------|--------|
| `create_console_config()` | Console only |
| `create_file_config()` | File only |
| `create_console_file_config()` | Console + File |
| `create_console_datadog_config()` | Console + Datadog |
| `create_file_datadog_config()` | File + Datadog |
| `create_console_file_datadog_config()` | All three |

### Examples

```python
from dc_logger import (
    create_console_config,
    create_file_config,
    create_console_file_config,
    create_console_datadog_config,
    LogLevel
)

# Console only
console = create_console_config(level=LogLevel.DEBUG)

# File only
file = create_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO
)

# Console + File
both = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO,
    pretty_print=True
)

# Console + Datadog
cloud = create_console_datadog_config(
    datadog_api_key="key",
    datadog_service="service",
    datadog_env="prod"
)
```

## Common Settings

### Log Level

```python
from dc_logger import LogLevel

# Available levels (in order of severity)
LogLevel.DEBUG      # Most verbose
LogLevel.INFO       # Normal operations
LogLevel.WARNING    # Potential issues
LogLevel.ERROR      # Errors
LogLevel.CRITICAL   # Critical failures
```

### Batch Size and Flush Interval

```python
config = ConsoleLogConfig(
    batch_size=50,        # Flush every 50 logs
    flush_interval=10,    # Or every 10 seconds
    max_buffer_size=500   # Maximum logs to buffer
)
```

### Correlation Tracking

```python
config = ConsoleLogConfig(
    correlation_enabled=True  # Enable trace/span IDs
)
```

## Environment-Specific Configurations

### Using Environment Variables

```python
import os
from dc_logger import ConsoleLogConfig, LogLevel, create_console_datadog_config

env = os.getenv("ENVIRONMENT", "development")

if env == "production":
    config = create_console_datadog_config(
        datadog_api_key=os.getenv("DATADOG_API_KEY"),
        datadog_service=os.getenv("SERVICE_NAME", "my-app"),
        datadog_env="production",
        level=LogLevel.INFO
    )
elif env == "staging":
    config = create_console_file_config(
        file_path="logs/staging.log",
        level=LogLevel.DEBUG,
        pretty_print=False
    )
else:
    # Development
    config = ConsoleLogConfig(
        level=LogLevel.DEBUG,
        pretty_print=True
    )
```

### Configuration Factory Pattern

```python
from dc_logger import (
    LogConfig,
    ConsoleLogConfig,
    LogLevel,
    create_console_datadog_config,
    create_console_file_config
)

def get_logger_config(environment: str) -> LogConfig:
    """Get logger configuration based on environment."""
    configs = {
        "production": lambda: create_console_datadog_config(
            datadog_api_key=os.getenv("DATADOG_API_KEY"),
            datadog_service="my-app",
            datadog_env="production",
            level=LogLevel.INFO
        ),
        "staging": lambda: create_console_file_config(
            file_path="logs/staging.log",
            level=LogLevel.DEBUG
        ),
        "development": lambda: ConsoleLogConfig(
            level=LogLevel.DEBUG,
            pretty_print=True
        )
    }
    
    factory = configs.get(environment, configs["development"])
    return factory()
```

## See Also

- [Getting Started](./getting-started.md) - Basic setup
- [Best Practices](./best-practices.md) - Recommended patterns
- [API Reference](../API_REFERENCE.md) - Complete API documentation
