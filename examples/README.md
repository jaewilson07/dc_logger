# DC Logger Examples

This directory contains runnable example scripts demonstrating various features of the dc_logger library.

## Quick Start

Install dc_logger first:
```bash
pip install dc_logger
```

Then run any example:
```bash
python basic_usage.py
python advanced_logging.py
python custom_handlers.py
```

## Example Scripts

### `basic_usage.py`
**Difficulty:** Beginner

Demonstrates fundamental dc_logger usage:
- Creating a logger with console output
- Logging at different levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Adding context to log messages
- Using LogEntity for structured entity logging
- Proper cleanup with `logger.close()`

```bash
python basic_usage.py
```

### `advanced_logging.py`
**Difficulty:** Intermediate to Advanced

Demonstrates advanced features:
- Multi-handler configuration (console + file)
- HTTP details logging for API monitoring
- Correlation tracking for distributed tracing
- Multi-tenant context for SaaS applications
- Using `@log_call` decorator with sensitive parameter masking
- Error handling patterns

```bash
python advanced_logging.py
```

### `custom_handlers.py`
**Difficulty:** Intermediate

Demonstrates handler configurations:
- Console handler with JSON and text formats
- File handler setup
- Multi-handler configuration
- Batch size and flush interval options
- Log level filtering
- Colored console output

```bash
python custom_handlers.py
```

### `example_console_colors.py`
**Difficulty:** Beginner

Demonstrates console color features:
- Default colors based on log level
- Custom colors for messages
- Styled colors (bold, dim, etc.)
- Using colors with decorators

### `example_datadog_simple.py`
**Difficulty:** Intermediate

Demonstrates Datadog integration:
- Setting up Datadog handler
- Sending logs to Datadog
- Environment and service tagging

### `example_enhanced_logging.py`
**Difficulty:** Intermediate

Demonstrates enhanced logging features:
- `level_name` for custom categorization
- Optional `action` field
- Method passing for HTTP operations

### `example_global_logger_injection.py`
**Difficulty:** Intermediate

Demonstrates global logger patterns:
- Setting up a global logger
- Logger injection in decorators
- Accessing logger across modules

## Jupyter Notebooks

For interactive examples, see the Jupyter notebooks:

| Notebook | Description |
|----------|-------------|
| `01_basic_logs.ipynb` | Introduction to basic logging |
| `02_extractors.ipynb` | Custom entity and context extractors |
| `03_decorators.ipynb` | Using the `@log_call` decorator |
| `04_console_logging.ipynb` | Console output configuration |
| `05_file_logging.ipynb` | File logging setup |
| `06_cloud_logging.ipynb` | Cloud provider integrations |
| `07_multi_handler.ipynb` | Multi-handler configuration |

## Common Patterns

### Quick Console Logging
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

### Using the Global Logger
```python
from dc_logger import get_logger

logger = get_logger("my_app")
# Now use logger anywhere in your code
```

### Decorator-based Logging
```python
from dc_logger import log_call

@log_call(action_name="process", include_params=True)
async def process_data(data_id: str):
    return {"status": "done"}
```

## See Also

- [USAGE.md](../USAGE.md) - Comprehensive usage guide
- [API_REFERENCE.md](../API_REFERENCE.md) - Complete API documentation
- [.ai/context.md](../.ai/context.md) - Quick reference for AI agents
