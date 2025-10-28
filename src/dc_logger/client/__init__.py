"""Client module - Core data models, exceptions, and utilities"""

from .enums import LogLevel
from .exceptions import (
    LoggingError,
    LogHandlerError,
    LogConfigError,
    LogWriteError,
    LogFlushError
)
from .models import (
    LogEntity,
    HTTPDetails,
    Correlation,
    MultiTenant,
    LogEntry,
    CorrelationManager,
    correlation_manager
)

__all__ = [
    # Enums
    'LogLevel',
    
    # Exceptions
    'LoggingError',
    'LogHandlerError',
    'LogConfigError',
    'LogWriteError',
    'LogFlushError',
    
    # Models
    'LogEntity',
    'HTTPDetails',
    'Correlation',
    'MultiTenant',
    'LogEntry',
    
    # Correlation
    'CorrelationManager',
    'correlation_manager',
]