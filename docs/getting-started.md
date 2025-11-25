# Getting Started with DC Logger

A step-by-step introduction to the dc_logger library.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### Basic Installation

```bash
pip install dc_logger
```

### With Optional Dependencies

```bash
# With Datadog support
pip install dc_logger[datadog]

# With development tools
pip install dc_logger[dev]

# With all extras
pip install dc_logger[all]
```

### From Source

```bash
git clone https://github.com/jaewilson07/dc_logger.git
cd dc_logger
pip install -e .
```

## Your First Logger

### Step 1: Import the Library

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel
```

### Step 2: Create a Configuration

```python
# Create a console configuration
config = ConsoleLogConfig(
    level=LogLevel.INFO,    # Minimum level to log
    pretty_print=True       # Nice formatting for development
)
```

### Step 3: Create the Logger

```python
# Create the logger with your app name
logger = DCLogger(config, app_name="my_first_app")
```

### Step 4: Log Messages

```python
async def main():
    await logger.info("Hello, dc_logger!")
    await logger.warning("This is a warning")
    await logger.error("Something went wrong")
    
    # Always close when done
    await logger.close()

asyncio.run(main())
```

### Complete Example

```python
import asyncio
from dc_logger import DCLogger, ConsoleLogConfig, LogLevel

async def main():
    # Configure
    config = ConsoleLogConfig(level=LogLevel.INFO, pretty_print=True)
    
    # Create logger
    logger = DCLogger(config, "my_first_app")
    
    # Log messages
    await logger.info("Application started")
    await logger.info("Processing data", extra={"items": 100})
    await logger.warning("Memory usage high", extra={"usage": "85%"})
    
    # Cleanup
    await logger.close()

asyncio.run(main())
```

## Understanding Log Levels

DC Logger uses standard log levels in order of increasing severity:

| Level | When to Use | Example |
|-------|-------------|---------|
| `DEBUG` | Detailed debugging info | Variable values, flow control |
| `INFO` | General operational info | "User logged in", "Job started" |
| `WARNING` | Potential issues | "Disk space low", "Deprecated API" |
| `ERROR` | Errors that need attention | "Database connection failed" |
| `CRITICAL` | System-level failures | "Service unavailable" |

### Level Filtering

When you set a log level, messages at that level and above are logged:

```python
# Only WARNING, ERROR, and CRITICAL messages
config = ConsoleLogConfig(level=LogLevel.WARNING)

# All messages including DEBUG
config = ConsoleLogConfig(level=LogLevel.DEBUG)
```

## Using the Global Logger

For simpler applications, use the global logger:

```python
from dc_logger import get_logger

# Get the global logger (auto-configured)
logger = get_logger("my_app")

async def some_function():
    await logger.info("Using global logger")
```

## Adding Context to Logs

### Basic Context

```python
await logger.info(
    "User action",
    user="alice@example.com",
    action="login",
    duration_ms=150
)
```

### Entity Context

```python
from dc_logger import LogEntity

entity = LogEntity(
    type="dataset",
    id="ds_12345",
    name="Sales Data"
)

await logger.info("Dataset updated", entity=entity)
```

### Extra Metadata

```python
await logger.info(
    "File processed",
    extra={
        "filename": "data.csv",
        "rows": 10000,
        "size_mb": 25.5
    }
)
```

## Using Decorators

Automatically log function calls:

```python
from dc_logger import log_call

@log_call(action_name="process", include_params=True)
async def process_data(data_id: str):
    # Function automatically logged on entry and exit
    return {"status": "done"}
```

## Next Steps

Now that you have the basics, explore:

1. **[Configuration Guide](./configuration.md)** - All configuration options
2. **[Best Practices](./best-practices.md)** - Recommended patterns
3. **[USAGE.md](../USAGE.md)** - Comprehensive usage examples
4. **[API Reference](../API_REFERENCE.md)** - Complete API documentation

## Troubleshooting

### "No event loop" Error

DC Logger is async-first. Make sure you're running in an async context:

```python
import asyncio

async def main():
    # Your logging code here
    pass

asyncio.run(main())
```

### Logs Not Appearing

Check your log level:

```python
# DEBUG shows everything
config = ConsoleLogConfig(level=LogLevel.DEBUG)

# INFO hides DEBUG messages
config = ConsoleLogConfig(level=LogLevel.INFO)
```

### Missing Logs on Exit

Always close the logger to flush buffered logs:

```python
await logger.close()
```

Or use a try/finally:

```python
try:
    await logger.info("Working...")
finally:
    await logger.close()
```
