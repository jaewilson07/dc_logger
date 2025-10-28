"""Client module - Core data models, exceptions, and utilities"""

from .enums import LogLevel
from .exceptions import (
    LogConfigError,
    LogFlushError,
    LoggingError,
    LogHandlerError,
    LogWriteError,
)
from .models import (
    Correlation,
    CorrelationManager,
    HTTPDetails,
    LogEntity,
    LogEntry,
    MultiTenant,
    correlation_manager,
)

__all__ = [
    # Enums
    "LogLevel",
    # Exceptions
    "LoggingError",
    "LogHandlerError",
    "LogConfigError",
    "LogWriteError",
    "LogFlushError",
    # Models
    "LogEntity",
    "HTTPDetails",
    "Correlation",
    "MultiTenant",
    "LogEntry",
    # Correlation
    "CorrelationManager",
    "correlation_manager",
]
