"""
Logging level enumeration for dc_logger.

This module defines the standard log levels used throughout the dc_logger library.

Example:
    >>> from dc_logger import LogLevel
    >>> level = LogLevel.INFO
    >>> level.should_log(LogLevel.WARNING)  # True, INFO logs WARNING
    True
    >>> level.should_log(LogLevel.DEBUG)  # False, INFO doesn't log DEBUG
    False
"""

from enum import Enum


class LogLevel(str, Enum):
    """
    Standard logging levels for dc_logger.

    Log levels are ordered by severity from least to most severe:
    DEBUG < INFO < WARNING < ERROR < CRITICAL

    When a logger is configured with a level, it will only log messages
    at that level or higher severity.

    Attributes:
        DEBUG: Detailed debugging information for diagnosing problems.
        INFO: General informational messages about normal operations.
        WARNING: Warning messages for potential issues that may need attention.
        ERROR: Error messages for failures that need to be addressed.
        CRITICAL: Critical errors that may cause the system to stop working.

    Example:
        >>> from dc_logger import LogLevel, ConsoleLogConfig
        >>> # Only log WARNING and above
        >>> config = ConsoleLogConfig(level=LogLevel.WARNING)
        >>> # Convert from string
        >>> level = LogLevel.from_string("info")
        >>> level
        <LogLevel.INFO: 'INFO'>
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_string(cls, level_str: str) -> "LogLevel":
        """
        Convert a string to LogLevel enum.

        Args:
            level_str: String representation of the level (case-insensitive).

        Returns:
            LogLevel: The corresponding LogLevel enum value.
                Returns INFO if the string doesn't match any level.

        Example:
            >>> LogLevel.from_string("debug")
            <LogLevel.DEBUG: 'DEBUG'>
            >>> LogLevel.from_string("UNKNOWN")
            <LogLevel.INFO: 'INFO'>
        """
        try:
            return cls(level_str.upper())
        except ValueError:
            return cls.INFO  # default fallback

    def should_log(self, other: "LogLevel") -> bool:
        """
        Check if this level should log messages at the other level.

        A logger configured at a certain level will log messages at that
        level and all higher severity levels.

        Args:
            other: The level of the message being logged.

        Returns:
            bool: True if messages at `other` level should be logged.

        Example:
            >>> LogLevel.INFO.should_log(LogLevel.WARNING)
            True  # INFO logger will log WARNING messages
            >>> LogLevel.WARNING.should_log(LogLevel.DEBUG)
            False  # WARNING logger will not log DEBUG messages
        """
        levels = list(LogLevel)
        return levels.index(self) <= levels.index(other)
