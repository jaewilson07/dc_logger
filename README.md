# DC Logger

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A flexible, async-first structured logging library for Python with support for multiple handlers, cloud providers, distributed tracing, and multi-tenancy.

## Features

- **Async-first design** - Non-blocking logging for high-performance applications
- **Structured logging** - JSON-based logs with entities, actions, and context
- **Multiple handlers** - Console, file, and cloud output simultaneously
- **Cloud integrations** - Datadog, AWS CloudWatch, GCP, Azure support
- **Distributed tracing** - Built-in correlation with trace/span IDs
- **Decorator logging** - Automatic function entry/exit logging with `@log_call`
- **Multi-tenant support** - Tenant context for SaaS applications
- **Colored console output** - ANSI colors for better visibility

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
    config = ConsoleLogConfig(level=LogLevel.INFO)
    logger = DCLogger(config, "my_app")
    
    await logger.info("Application started")
    await logger.warning("This is a warning")
    await logger.error("Something went wrong")
    
    await logger.close()

asyncio.run(main())
```

## Using the Decorator

```python
from dc_logger import log_call

@log_call(action_name="process", include_params=True)
async def process_data(data_id: str):
    # Automatically logs entry, exit, duration, and errors
    return {"status": "processed"}
```

## Structured Logging with Context

```python
from dc_logger import LogEntity

entity = LogEntity(type="dataset", id="ds_123", name="Sales Data")

await logger.info(
    "Dataset processed",
    entity=entity,
    action="process_dataset",
    duration_ms=1500,
    extra={"rows": 10000}
)
```

## Multi-Handler Configuration

```python
from dc_logger import create_console_file_config

config = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO,
    pretty_print=True
)
logger = DCLogger(config, "my_app")
```

## Documentation

| Document | Description |
|----------|-------------|
| [USAGE.md](./USAGE.md) | Comprehensive usage guide |
| [API_REFERENCE.md](./API_REFERENCE.md) | Complete API documentation |
| [docs/getting-started.md](./docs/getting-started.md) | Step-by-step introduction |
| [docs/configuration.md](./docs/configuration.md) | Configuration options |
| [docs/best-practices.md](./docs/best-practices.md) | Recommended patterns |
| [examples/](./examples/) | Working example scripts |

### For AI Agents

See [.ai/context.md](./.ai/context.md) for a quick reference guide optimized for AI agents.

## Key Components

| Component | Import | Description |
|-----------|--------|-------------|
| `DCLogger` | `from dc_logger import DCLogger` | Main logger class |
| `ConsoleLogConfig` | `from dc_logger import ConsoleLogConfig` | Console configuration |
| `LogLevel` | `from dc_logger import LogLevel` | Log levels (DEBUG, INFO, etc.) |
| `LogEntity` | `from dc_logger import LogEntity` | Entity context for logs |
| `HTTPDetails` | `from dc_logger import HTTPDetails` | HTTP request details |
| `log_call` | `from dc_logger import log_call` | Function logging decorator |
| `get_logger` | `from dc_logger import get_logger` | Get global logger |
| `correlation_manager` | `from dc_logger import correlation_manager` | Distributed tracing |

## Log Levels

```python
LogLevel.DEBUG      # Detailed debugging information
LogLevel.INFO       # General informational messages
LogLevel.WARNING    # Warning messages for potential issues
LogLevel.ERROR      # Error messages for failures
LogLevel.CRITICAL   # Critical errors requiring immediate attention
```

## Cloud Integrations

### Datadog

```python
from dc_logger import create_console_datadog_config

config = create_console_datadog_config(
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production"
)
```

## Architecture

See [documentation/architecture.md](./documentation/architecture.md) for design details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Jae Wilson ([@jaewilson07](https://github.com/jaewilson07))
