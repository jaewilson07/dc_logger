# DC Logger API Reference

Complete API documentation for the dc_logger library.

## Table of Contents

- [Core Classes](#core-classes)
  - [DCLogger](#dclogger)
  - [LogLevel](#loglevel)
  - [LogEntry](#logentry)
  - [LogEntity](#logentity)
  - [HTTPDetails](#httpdetails)
  - [Correlation](#correlation)
  - [MultiTenant](#multitenant)
  - [CorrelationManager](#correlationmanager)
- [Configuration Classes](#configuration-classes)
  - [LogConfig](#logconfig)
  - [ConsoleLogConfig](#consolelogconfig)
  - [DatadogLogConfig](#datadoglogconfig)
  - [MultiHandlerLogConfig](#multihandlerlogconfig)
- [Decorators](#decorators)
  - [log_call](#log_call)
  - [LogDecoratorConfig](#logdecoratorconfig)
- [Factory Functions](#factory-functions)
- [Handlers](#handlers)
- [Utility Functions](#utility-functions)

---

## Core Classes

### DCLogger

The main logger class for structured logging with multiple handlers.

```python
from dc_logger import DCLogger
```

#### Constructor

```python
DCLogger(config: LogConfig, app_name: str)
```

**Parameters:**
- `config` (`LogConfig`): Configuration object for the logger
- `app_name` (`str`): Name of the application for log identification

**Example:**
```python
from dc_logger import DCLogger, ConsoleLogConfig

config = ConsoleLogConfig(level=LogLevel.INFO)
logger = DCLogger(config, "my_app")
```

#### Methods

##### `async log(level: LogLevel, message: str, **context) -> bool`

Log a message with structured context.

**Parameters:**
- `level` (`LogLevel`): The log level for this message
- `message` (`str`): The log message
- `**context`: Additional context including:
  - `logger` (`str`, optional): Custom logger name
  - `user` (`str`, optional): User identifier
  - `action` (`str`, optional): Action being performed
  - `entity` (`LogEntity`, optional): Entity being operated on
  - `status` (`str`, optional): Status of the operation (default: "info")
  - `duration_ms` (`int`, optional): Duration in milliseconds
  - `multi_tenant` (`MultiTenant`, optional): Multi-tenant context
  - `http_details` (`HTTPDetails`, optional): HTTP request/response details
  - `extra` (`dict`, optional): Additional metadata
  - `color` (`str`, optional): Console output color

**Returns:** `bool` - True if logging succeeded

**Example:**
```python
await logger.log(
    LogLevel.INFO,
    "User action completed",
    user="user@example.com",
    action="update_profile",
    duration_ms=150
)
```

##### `async debug(message: str, **context) -> bool`

Log a DEBUG level message.

**Example:**
```python
await logger.debug("Processing item", item_id="123")
```

##### `async info(message: str, **context) -> bool`

Log an INFO level message.

**Example:**
```python
await logger.info("Application started")
```

##### `async warning(message: str, **context) -> bool`

Log a WARNING level message.

**Example:**
```python
await logger.warning("Resource usage high", usage_percent=85)
```

##### `async error(message: str, **context) -> bool`

Log an ERROR level message.

**Example:**
```python
await logger.error("Operation failed", error_code="E001")
```

##### `async critical(message: str, **context) -> bool`

Log a CRITICAL level message.

**Example:**
```python
await logger.critical("System failure", component="database")
```

##### `async flush() -> bool`

Flush buffered log entries to all handlers.

**Returns:** `bool` - True if all handlers flushed successfully

**Example:**
```python
await logger.flush()
```

##### `async close() -> None`

Clean up resources and close all handlers.

**Example:**
```python
await logger.close()
```

##### `start_request(parent_trace_id: Optional[str] = None, auth: Any = None) -> str`

Start a new request context for correlation tracking.

**Parameters:**
- `parent_trace_id` (`str`, optional): Parent trace ID for distributed tracing
- `auth` (`Any`, optional): Authentication context

**Returns:** `str` - The request ID

**Example:**
```python
request_id = logger.start_request()
```

##### `end_request() -> None`

End the current request context.

**Example:**
```python
logger.end_request()
```

---

### LogLevel

Enumeration of standard logging levels.

```python
from dc_logger import LogLevel
```

#### Values

| Level | Value | Description |
|-------|-------|-------------|
| `DEBUG` | "DEBUG" | Detailed debugging information |
| `INFO` | "INFO" | General informational messages |
| `WARNING` | "WARNING" | Warning messages for potential issues |
| `ERROR` | "ERROR" | Error messages for failures |
| `CRITICAL` | "CRITICAL" | Critical errors requiring immediate attention |

#### Methods

##### `from_string(level_str: str) -> LogLevel`

Convert a string to LogLevel enum.

**Parameters:**
- `level_str` (`str`): String representation of the level

**Returns:** `LogLevel` - The corresponding LogLevel (defaults to INFO)

**Example:**
```python
level = LogLevel.from_string("DEBUG")
```

##### `should_log(other: LogLevel) -> bool`

Check if this level should log messages at the other level.

**Parameters:**
- `other` (`LogLevel`): The level to compare against

**Returns:** `bool` - True if messages at `other` level should be logged

**Example:**
```python
if LogLevel.INFO.should_log(LogLevel.DEBUG):
    # Would be False - INFO doesn't log DEBUG messages
    pass
```

---

### LogEntry

Structured log entry with all contextual information.

```python
from dc_logger import LogEntry
```

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `timestamp` | `str` | ISO format timestamp |
| `level` | `LogLevel` | Log level |
| `message` | `str` | Log message |
| `method` | `str` | HTTP method or "COMMENT" |
| `app_name` | `str` | Application name |
| `user` | `str`, optional | User identifier |
| `action` | `str`, optional | Action being performed |
| `level_name` | `str`, optional | Custom level name |
| `entity` | `LogEntity`, optional | Entity information |
| `status` | `str` | Status ("info", "success", "error") |
| `duration_ms` | `int`, optional | Duration in milliseconds |
| `correlation` | `Correlation`, optional | Correlation IDs |
| `multi_tenant` | `MultiTenant`, optional | Multi-tenant context |
| `http_details` | `HTTPDetails`, optional | HTTP details |
| `extra` | `dict` | Additional metadata |
| `color` | `str`, optional | Console output color |

#### Methods

##### `create(level: LogLevel, message: str, app_name: str = "default", **kwargs) -> LogEntry`

Factory method to create a LogEntry with current timestamp.

**Example:**
```python
entry = LogEntry.create(
    level=LogLevel.INFO,
    message="User logged in",
    app_name="my_app",
    user="user@example.com"
)
```

##### `to_dict() -> Dict[str, Any]`

Convert to dictionary for JSON serialization.

**Example:**
```python
log_dict = entry.to_dict()
```

##### `to_json() -> str`

Convert to JSON string.

**Example:**
```python
json_str = entry.to_json()
```

---

### LogEntity

Entity information for logging.

```python
from dc_logger import LogEntity
```

#### Constructor

```python
LogEntity(
    type: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    additional_info: Dict[str, Any] = None
)
```

**Parameters:**
- `type` (`str`): Entity type (e.g., "dataset", "user", "card")
- `id` (`str`, optional): Entity identifier
- `name` (`str`, optional): Entity name
- `additional_info` (`dict`, optional): Additional metadata

**Example:**
```python
entity = LogEntity(
    type="dataset",
    id="ds_12345",
    name="Sales Data",
    additional_info={"owner": "analytics_team"}
)
```

#### Methods

##### `from_any(obj: Any) -> Optional[LogEntity]`

Create LogEntity from dict or existing LogEntity.

**Example:**
```python
entity = LogEntity.from_any({"type": "user", "id": "123"})
```

##### `to_dict() -> Dict[str, Any]`

Convert to dictionary.

**Example:**
```python
entity_dict = entity.to_dict()
```

---

### HTTPDetails

HTTP request/response details for logging.

```python
from dc_logger import HTTPDetails
```

#### Constructor

```python
HTTPDetails(
    method: Optional[str] = None,
    url: Optional[str] = None,
    status_code: Optional[int] = None,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    response_size: Optional[int] = None,
    request_body: Optional[Any] = None,
    response_body: Optional[Any] = None
)
```

**Example:**
```python
http = HTTPDetails(
    method="POST",
    url="/api/v1/datasets",
    status_code=201,
    response_size=1024
)
```

#### Methods

##### `from_kwargs(kwargs: Dict[str, Any]) -> Optional[HTTPDetails]`

Create HTTPDetails from kwargs dictionary.

##### `to_dict() -> Dict[str, Any]`

Convert to dictionary.

---

### Correlation

Correlation information for distributed tracing.

```python
from dc_logger import Correlation
```

#### Constructor

```python
Correlation(
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    parent_span_id: Optional[str] = None
)
```

**Example:**
```python
correlation = Correlation(
    trace_id="abc123",
    span_id="span456",
    parent_span_id="parent789"
)
```

---

### MultiTenant

Multi-tenant context information.

```python
from dc_logger import MultiTenant
```

#### Constructor

```python
MultiTenant(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    organization_id: Optional[str] = None
)
```

**Example:**
```python
tenant = MultiTenant(
    user_id="user123",
    tenant_id="tenant456",
    organization_id="org789"
)
```

---

### CorrelationManager

Manages correlation IDs and context propagation.

```python
from dc_logger import correlation_manager
```

#### Methods

##### `generate_trace_id() -> str`

Generate a new trace ID (UUID).

##### `generate_request_id() -> str`

Generate a new request ID (12-character hex).

##### `generate_span_id() -> str`

Generate a new span ID (16-character hex).

##### `generate_session_id() -> str`

Generate a new session ID (12-character hex).

##### `get_or_create_correlation() -> Correlation`

Get or create correlation with automatic span chaining.

**Example:**
```python
correlation = correlation_manager.get_or_create_correlation()
print(f"Trace: {correlation.trace_id}")
print(f"Span: {correlation.span_id}")
```

##### `start_new_trace() -> str`

Start a completely new trace, clearing existing context.

**Returns:** The new trace ID

##### `start_request(parent_trace_id: Optional[str] = None, auth: Any = None, is_pagination_request: bool = False) -> str`

Start a new request context.

**Returns:** The request ID

##### `get_current_context() -> Dict[str, Any]`

Get current correlation context.

**Returns:** Dictionary with trace_id, request_id, session_id, span_id, correlation

---

## Configuration Classes

### LogConfig

Abstract base configuration class.

```python
from dc_logger import LogConfig
```

#### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | `LogLevel` | `LogLevel.INFO` | Minimum log level |
| `output_mode` | `str` | "console" | Output mode: "cloud", "console", "file", "multi" |
| `format` | `str` | "json" | Output format: "json", "text" |
| `destination` | `str`, optional | None | File path, webhook URL, etc. |
| `batch_size` | `int` | 100 | Logs to buffer before flush |
| `flush_interval` | `int` | 30 | Seconds between auto-flushes |
| `correlation_enabled` | `bool` | True | Enable correlation tracking |
| `include_traceback` | `bool` | True | Include stack traces |
| `max_buffer_size` | `int` | 1000 | Maximum buffer size |
| `pretty_print` | `bool` | False | Pretty print JSON |

---

### ConsoleLogConfig

Console-specific log configuration.

```python
from dc_logger import ConsoleLogConfig
```

**Example:**
```python
config = ConsoleLogConfig(
    level=LogLevel.DEBUG,
    pretty_print=True,
    format="json"
)
```

---

### DatadogLogConfig

Datadog-specific log configuration.

```python
from dc_logger import DatadogLogConfig
```

#### Additional Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `api_key` | `str` | Datadog API key |
| `service` | `str` | Service name |
| `env` | `str` | Environment (e.g., "production") |
| `source` | `str` | Log source identifier |
| `hostname` | `str`, optional | Hostname |
| `tags` | `list`, optional | Additional tags |

**Example:**
```python
config = DatadogLogConfig(
    api_key="your-api-key",
    service="my-service",
    env="production",
    level=LogLevel.INFO
)
```

---

### MultiHandlerLogConfig

Configuration for multiple handlers.

```python
from dc_logger import MultiHandlerLogConfig, HandlerConfig
```

**Example:**
```python
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

---

## Decorators

### log_call

Decorator for automatic function call logging.

```python
from dc_logger import log_call
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `func` | `Callable`, optional | None | Function to decorate |
| `logger` | `Any`, optional | None | Direct logger instance |
| `logger_getter` | `Callable`, optional | None | Callable that returns a logger |
| `action_name` | `str`, optional | None | Custom action name |
| `level_name` | `str`, optional | None | Custom level name |
| `log_level` | `LogLevel` | `LogLevel.INFO` | Minimum log level |
| `include_params` | `bool` | False | Include function parameters |
| `sensitive_params` | `list`, optional | None | Parameters to sanitize |
| `config` | `LogDecoratorConfig`, optional | None | Advanced configuration |
| `color` | `str`, optional | None | Console output color |

**Example:**
```python
@log_call(action_name="process_data", include_params=True)
async def process_data(data_id: str):
    return {"status": "processed"}
```

---

### LogDecoratorConfig

Advanced configuration for log_call decorator.

```python
from dc_logger import LogDecoratorConfig
```

#### Constructor

```python
LogDecoratorConfig(
    action_name: Optional[str] = None,
    level_name: Optional[str] = None,
    log_level: LogLevel = LogLevel.INFO,
    entity_extractor: Optional[EntityExtractor] = None,
    http_extractor: Optional[HTTPDetailsExtractor] = None,
    multitenant_extractor: Optional[MultiTenantExtractor] = None,
    result_processor: Optional[ResultProcessor] = None,
    include_params: bool = False,
    sensitive_params: Optional[list] = None,
    color: Optional[str] = None
)
```

---

## Factory Functions

### create_console_config

```python
from dc_logger import create_console_config

config = create_console_config(
    level=LogLevel.INFO,
    pretty_print=False
)
```

### create_file_config

```python
from dc_logger import create_file_config

config = create_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO
)
```

### create_console_file_config

```python
from dc_logger import create_console_file_config

config = create_console_file_config(
    file_path="logs/app.log",
    level=LogLevel.INFO,
    pretty_print=True
)
```

### create_console_datadog_config

```python
from dc_logger import create_console_datadog_config

config = create_console_datadog_config(
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production"
)
```

### create_console_file_datadog_config

```python
from dc_logger import create_console_file_datadog_config

config = create_console_file_datadog_config(
    file_path="logs/app.log",
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production"
)
```

### create_file_datadog_config

```python
from dc_logger import create_file_datadog_config

config = create_file_datadog_config(
    file_path="logs/app.log",
    datadog_api_key="your-api-key",
    datadog_service="my-service",
    datadog_env="production"
)
```

---

## Handlers

### LogHandler (Base)

Abstract base class for all handlers.

**Methods:**
- `async write(entries: List[LogEntry]) -> bool`
- `async flush() -> bool`
- `async close() -> None`

### ConsoleHandler

Writes logs to stdout.

### FileHandler

Writes logs to a file.

### DatadogHandler

Sends logs to Datadog.

### AWSCloudWatchHandler

Sends logs to AWS CloudWatch (placeholder).

### GCPLoggingHandler

Sends logs to Google Cloud Logging (placeholder).

### AzureLogAnalyticsHandler

Sends logs to Azure Log Analytics (placeholder).

---

## Utility Functions

### get_logger

```python
from dc_logger import get_logger

logger = get_logger("my_app")
```

Get or create the global logger instance.

**Parameters:**
- `app_name` (`str`): Application name (default: "domolibrary")

**Returns:** `DCLogger` instance

### set_global_logger

```python
from dc_logger import set_global_logger

set_global_logger(my_custom_logger)
```

Set the global logger instance.

**Parameters:**
- `logger` (`DCLogger`): Logger instance to set as global

### extract_entity_from_args

```python
from dc_logger import extract_entity_from_args

entity = extract_entity_from_args(args, kwargs)
```

Extract entity information from function arguments.

**Parameters:**
- `args`: Positional arguments
- `kwargs`: Keyword arguments

**Returns:** `LogEntity` or None

---

## See Also

- [Usage Guide](./USAGE.md) - Comprehensive usage examples
- [Examples](./examples/) - Working example scripts
- [AI Agent Guide](./.ai/context.md) - Quick reference for AI agents
