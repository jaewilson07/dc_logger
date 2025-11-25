"""
DC_Logger - Enhanced Structured Logging System

This is the main logger implementation that provides structured logging
with support for multiple handlers, correlation tracking, and cloud integrations.

The DCLogger class is the primary entry point for logging operations. It supports:
- Async logging methods (debug, info, warning, error, critical)
- Multiple output handlers (console, file, cloud)
- Automatic buffering and flushing
- Correlation tracking for distributed tracing

Example:
    >>> import asyncio
    >>> from dc_logger import DCLogger, ConsoleLogConfig, LogLevel
    >>>
    >>> async def main():
    ...     config = ConsoleLogConfig(level=LogLevel.INFO)
    ...     logger = DCLogger(config, "my_app")
    ...     await logger.info("Application started")
    ...     await logger.close()
    >>>
    >>> asyncio.run(main())

Note:
    All logging methods are async and must be awaited. Always call
    logger.close() when shutting down to ensure all buffered logs are flushed.
"""

import asyncio
from asyncio import Task
from typing import Any, List, Optional

from .client.enums import LogLevel
from .client.exceptions import LogConfigError
from .client.models import LogEntry, correlation_manager
from .configs.base import LogConfig
from .configs.console import ConsoleLogConfig
from .handlers.base import LogHandler
from .handlers.cloud.aws import AWSCloudWatchHandler
from .handlers.cloud.azure import AzureLogAnalyticsHandler
from .handlers.cloud.datadog import DatadogHandler
from .handlers.cloud.gcp import GCPLoggingHandler
from .handlers.console import ConsoleHandler
from .handlers.file import FileHandler


class DCLogger:
    """
    Enhanced logger with structured logging and multiple handlers.

    The main logger class for dc_logger that provides async-first structured
    logging with support for multiple output handlers, correlation tracking,
    and automatic buffering.

    Args:
        config: Configuration object (ConsoleLogConfig, DatadogLogConfig, etc.)
        app_name: Name of the application for log identification

    Attributes:
        config: The logger configuration
        app_name: Application name used in logs
        handlers: List of active log handlers
        buffer: Buffer for pending log entries
        correlation_manager: Manager for distributed tracing

    Example:
        >>> import asyncio
        >>> from dc_logger import DCLogger, ConsoleLogConfig, LogLevel
        >>>
        >>> async def main():
        ...     config = ConsoleLogConfig(level=LogLevel.INFO)
        ...     logger = DCLogger(config, "my_app")
        ...
        ...     await logger.info("Hello, world!")
        ...     await logger.info("User logged in", user="alice@example.com")
        ...     await logger.error("Something failed", extra={"code": 500})
        ...
        ...     await logger.close()
        >>>
        >>> asyncio.run(main())

    Note:
        - All logging methods are async and must be awaited
        - Always call close() to flush buffered logs before shutdown
        - Use start_request()/end_request() for request lifecycle tracking
    """

    def __init__(self, config: LogConfig, app_name: str):
        """
        Initialize the DCLogger with configuration and app name.

        Args:
            config: A LogConfig instance (ConsoleLogConfig, DatadogLogConfig, etc.)
                that defines the logging behavior and output destinations.
            app_name: Name of the application, used as a prefix in log entries
                for identification in multi-service environments.

        Raises:
            LogConfigError: If the configuration is invalid.

        Example:
            >>> from dc_logger import DCLogger, ConsoleLogConfig, LogLevel
            >>> config = ConsoleLogConfig(level=LogLevel.DEBUG, pretty_print=True)
            >>> logger = DCLogger(config, "my_service")

        Note:
            The logger attempts to start a background flush task if an event loop
            is running. If not, the task starts on the first log call.
        """
        self.config = config
        self.app_name = app_name
        self.handlers: List[LogHandler] = []
        self.buffer: List[LogEntry] = []
        self.correlation_manager = correlation_manager
        self.flush_task: Optional[Task[None]] = None

        # Validate configuration
        config.validate_config()

        # Initialize handlers based on config
        self._setup_handlers()

        # Try to start background flush task if event loop is available
        try:
            asyncio.get_running_loop()
            self._start_flush_task()
        except RuntimeError:
            # No event loop, task will be started when first log is called
            pass

    def _setup_handlers(self) -> None:
        """
        Setup handlers based on configuration.

        Initializes the appropriate log handlers (console, file, cloud) based
        on the configuration provided to the logger.

        Raises:
            LogConfigError: If an unknown handler type or cloud provider is specified.
        """
        # Get handler configurations from the config
        handler_configs = self.config.get_handler_configs()

        for handler_config in handler_configs:
            handler_type = handler_config["type"]
            config = handler_config["config"]
            cloud_config = handler_config.get("cloud_config")

            if handler_type == "console":
                self.handlers.append(ConsoleHandler(config))
            elif handler_type == "file":
                self.handlers.append(FileHandler(config))
            elif handler_type == "cloud":
                if cloud_config:
                    cloud_provider = cloud_config.get("cloud_provider")
                    if cloud_provider == "datadog":
                        self.handlers.append(DatadogHandler(config))
                    elif cloud_provider == "aws":
                        self.handlers.append(AWSCloudWatchHandler(config))
                    elif cloud_provider == "gcp":
                        self.handlers.append(GCPLoggingHandler(config))
                    elif cloud_provider == "azure":
                        self.handlers.append(AzureLogAnalyticsHandler(config))
                    else:
                        raise LogConfigError(
                            f"Unknown cloud provider: {cloud_provider}"
                        )
                else:
                    raise LogConfigError("Cloud handler missing cloud_config")
            else:
                raise LogConfigError(f"Unknown handler type: {handler_type}")

    def _start_flush_task(self) -> None:
        """
        Start the background flush task.

        Creates an asyncio task that periodically flushes buffered log entries
        to all handlers based on the configured flush_interval.
        """
        if self.flush_task is None:
            self.flush_task = asyncio.create_task(self._periodic_flush())

    async def log(self, level: LogLevel, message: str, **context: Any) -> bool:
        """
        Log a message with structured context.

        Creates a log entry with the specified level, message, and context,
        then adds it to the buffer. The buffer is flushed when it reaches
        the configured batch_size.

        Args:
            level: The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            message: The log message text.
            **context: Additional context for the log entry:
                - logger (str): Custom logger name (default: "domolibrary.{app_name}")
                - user (str): User identifier
                - action (str): Action being performed
                - entity (LogEntity): Entity being operated on
                - status (str): Status of the operation (default: "info")
                - duration_ms (int): Duration in milliseconds
                - multi_tenant (MultiTenant): Multi-tenant context
                - http_details (HTTPDetails): HTTP request/response details
                - extra (dict): Additional metadata
                - color (str): Console output color

        Returns:
            bool: True if the log was successfully buffered.

        Example:
            >>> await logger.log(
            ...     LogLevel.INFO,
            ...     "User action completed",
            ...     user="alice@example.com",
            ...     action="update_profile",
            ...     duration_ms=150,
            ...     extra={"field": "email"}
            ... )
            True

        Note:
            Messages below the configured log level are silently ignored.
        """

        # Check if we should log this level
        if not self.config.level.should_log(level):
            return True

        # Start flush task if not already started and event loop is available
        if self.flush_task is None:
            try:
                asyncio.get_running_loop()
                self._start_flush_task()
            except RuntimeError:
                pass

        # Create log entry
        entry = LogEntry.create(
            level=level,
            message=message,
            logger=context.get("logger", f"domolibrary.{self.app_name}"),
            user=context.get("user"),
            action=context.get("action"),
            entity=context.get("entity"),
            status=context.get("status", "info"),
            duration_ms=context.get("duration_ms"),
            trace_id=self.correlation_manager.trace_id_var.get(),
            request_id=self.correlation_manager.request_id_var.get(),
            session_id=self.correlation_manager.session_id_var.get(),
            correlation=self.correlation_manager.correlation_var.get(),
            multi_tenant=context.get("multi_tenant"),
            http_details=context.get("http_details"),
            extra=context.get("extra", {}),
            color=context.get("color"),
        )

        # Add to buffer
        self.buffer.append(entry)

        # Flush if buffer is full
        if len(self.buffer) >= self.config.batch_size:
            await self.flush()

        return True

    async def flush(self) -> bool:
        """
        Flush buffered entries to all handlers.

        Immediately writes all buffered log entries to configured handlers.
        This is useful when you need to ensure logs are written before
        an operation completes.

        Returns:
            bool: True if all handlers successfully flushed.

        Example:
            >>> await logger.info("Important message")
            >>> await logger.flush()  # Ensure it's written immediately
            True

        Note:
            Logs are also auto-flushed based on batch_size and flush_interval.
        """
        if not self.buffer:
            return True

        entries_to_flush = self.buffer.copy()
        self.buffer.clear()

        success = True
        for handler in self.handlers:
            if not await handler.write(entries_to_flush):
                success = False

        return success

    async def _periodic_flush(self) -> None:
        """
        Background task to periodically flush logs.

        Runs continuously, flushing the buffer at intervals defined by
        config.flush_interval seconds.
        """
        while True:
            await asyncio.sleep(self.config.flush_interval)
            await self.flush()

    # Convenience methods for different log levels
    async def debug(self, message: str, **context: Any) -> bool:
        """
        Log a DEBUG level message.

        Args:
            message: The log message text.
            **context: Additional context (see log() for details).

        Returns:
            bool: True if logged successfully.

        Example:
            >>> await logger.debug("Processing item", item_id="123")
        """
        return await self.log(LogLevel.DEBUG, message, **context)

    async def info(self, message: str, **context: Any) -> bool:
        """
        Log an INFO level message.

        Args:
            message: The log message text.
            **context: Additional context (see log() for details).

        Returns:
            bool: True if logged successfully.

        Example:
            >>> await logger.info("User logged in", user="alice@example.com")
        """
        return await self.log(LogLevel.INFO, message, **context)

    async def warning(self, message: str, **context: Any) -> bool:
        """
        Log a WARNING level message.

        Args:
            message: The log message text.
            **context: Additional context (see log() for details).

        Returns:
            bool: True if logged successfully.

        Example:
            >>> await logger.warning("Resource usage high", usage_percent=85)
        """
        return await self.log(LogLevel.WARNING, message, **context)

    async def error(self, message: str, **context: Any) -> bool:
        """
        Log an ERROR level message.

        Args:
            message: The log message text.
            **context: Additional context (see log() for details).

        Returns:
            bool: True if logged successfully.

        Example:
            >>> await logger.error("Database connection failed", error_code="E001")
        """
        return await self.log(LogLevel.ERROR, message, **context)

    async def critical(self, message: str, **context: Any) -> bool:
        """
        Log a CRITICAL level message.

        Args:
            message: The log message text.
            **context: Additional context (see log() for details).

        Returns:
            bool: True if logged successfully.

        Example:
            >>> await logger.critical("Database unavailable", service="postgres")
        """
        return await self.log(LogLevel.CRITICAL, message, **context)

    def start_request(
        self, parent_trace_id: Optional[str] = None, auth: Any = None
    ) -> str:
        """
        Start a new request context for correlation tracking.

        Creates a new trace/span context for distributed tracing. Call this
        at the beginning of a request to track related log entries.

        Args:
            parent_trace_id: Parent trace ID from upstream service for
                distributed tracing continuity.
            auth: Authentication context (optional).

        Returns:
            str: The new request ID.

        Example:
            >>> request_id = logger.start_request()
            >>> # ... handle request ...
            >>> logger.end_request()
        """
        return self.correlation_manager.start_request(parent_trace_id, auth)

    def end_request(self) -> None:
        """
        End the current request context.

        Clears the request context. Context variables will be reset on the
        next start_request() call.
        """
        # Clear context variables (they'll be reset on next request)

    async def close(self) -> None:
        """
        Clean up resources and close all handlers.

        Cancels the background flush task, performs a final flush of any
        buffered logs, and closes all handlers. Always call this before
        shutting down the application.

        Example:
            >>> try:
            ...     await logger.info("Application running")
            ... finally:
            ...     await logger.close()

        Note:
            Failing to call close() may result in lost log entries.
        """
        # Cancel flush task
        if hasattr(self, "flush_task") and self.flush_task:
            self.flush_task.cancel()
            try:
                await self.flush_task
            except asyncio.CancelledError:
                pass

        # Final flush
        await self.flush()

        # Close handlers
        for handler in self.handlers:
            await handler.close()


# Global logger instance
_global_logger: Optional[DCLogger] = None


def get_logger(app_name: str = "domolibrary") -> DCLogger:
    """
    Get or create the global logger instance.

    Returns the existing global logger, or creates a new one with default
    console configuration if none exists.

    Args:
        app_name: Application name for the logger (default: "domolibrary").
            Only used when creating a new logger.

    Returns:
        DCLogger: The global logger instance.

    Example:
        >>> from dc_logger import get_logger
        >>> logger = get_logger("my_app")
        >>> await logger.info("Using global logger")

    Note:
        To customize the global logger, use set_global_logger() with a
        pre-configured DCLogger instance.
    """
    global _global_logger
    if _global_logger is None:
        config = ConsoleLogConfig(level=LogLevel.INFO, pretty_print=False)
        _global_logger = DCLogger(config, app_name)

    return _global_logger


def set_global_logger(logger: DCLogger) -> None:
    """
    Set the global logger instance.

    Replaces the global logger with a custom configured instance.
    Use this to customize the global logger behavior.

    Args:
        logger: A pre-configured DCLogger instance.

    Example:
        >>> from dc_logger import DCLogger, ConsoleLogConfig, LogLevel, set_global_logger
        >>> config = ConsoleLogConfig(level=LogLevel.DEBUG, pretty_print=True)
        >>> custom_logger = DCLogger(config, "my_app")
        >>> set_global_logger(custom_logger)
    """
    global _global_logger
    _global_logger = logger
