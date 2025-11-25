"""
DC Logger - Structured Logging System for Python Applications

A comprehensive, async-first logging framework with support for:
- Multiple output handlers (console, file, cloud)
- Structured logging with JSON support
- Correlation tracking for distributed tracing
- Cloud integrations (Datadog, AWS CloudWatch, GCP, Azure)
- Async and sync support
- Decorator-based automatic logging

Quick Start:
    >>> import asyncio
    >>> from dc_logger import DCLogger, ConsoleLogConfig, LogLevel
    >>>
    >>> async def main():
    ...     config = ConsoleLogConfig(level=LogLevel.INFO)
    ...     logger = DCLogger(config, "my_app")
    ...     await logger.info("Hello, dc_logger!")
    ...     await logger.close()
    >>>
    >>> asyncio.run(main())

Using the decorator:
    >>> from dc_logger import log_call
    >>>
    >>> @log_call(action_name="process", include_params=True)
    ... async def process_data(data_id: str):
    ...     return {"status": "processed"}

For more information, see:
- USAGE.md: Comprehensive usage guide
- API_REFERENCE.md: Complete API documentation
- .ai/context.md: Quick reference for AI agents
"""

from .client import (
    Correlation,
    HTTPDetails,
    LogEntity,
    LogEntry,
    LogLevel,
    MultiTenant,
    correlation_manager,
)
from .configs import (
    AWSCloudWatchLogConfig,
    AzureLogAnalyticsConfig,
    ConsoleLogConfig,
    DatadogLogConfig,
    GCPLoggingConfig,
    LogConfig,
    MultiHandlerLogConfig,
    create_console_config,
    create_console_datadog_config,
    create_console_file_config,
    create_console_file_datadog_config,
    create_file_config,
    create_file_datadog_config,
)
from .decorators import LogDecoratorConfig, log_call, log_function_call
from .logger import DCLogger, get_logger, set_global_logger
from .utils import extract_entity_from_args

__version__ = "1.1.1"

__all__ = [
    # Main logger
    "DCLogger",
    "get_logger",
    "set_global_logger",
    # Core types
    "LogLevel",
    "LogEntry",
    "LogEntity",
    "HTTPDetails",
    "Correlation",
    "MultiTenant",
    "correlation_manager",
    # Configurations
    "LogConfig",
    "ConsoleLogConfig",
    "DatadogLogConfig",
    "AWSCloudWatchLogConfig",
    "GCPLoggingConfig",
    "AzureLogAnalyticsConfig",
    "MultiHandlerLogConfig",
    # Factory functions
    "create_console_config",
    "create_file_config",
    "create_console_file_config",
    "create_console_datadog_config",
    "create_console_file_datadog_config",
    "create_file_datadog_config",
    # Decorators and utilities
    "log_call",
    "log_function_call",
    "LogDecoratorConfig",
    "extract_entity_from_args",
]
