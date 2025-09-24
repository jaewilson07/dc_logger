import os
from typing import Optional, List, Dict, Any, Literal
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..client.enums import LogLevel
from ..client.exceptions import LogConfigError


# Type for valid output modes
OutputMode = Literal["cloud", "console", "file"]


@dataclass
class LogConfig(ABC):
    """Abstract base configuration for logging system"""

    level: LogLevel = LogLevel.INFO
    output_mode: OutputMode = "console"  # cloud, console, or file
    format: str = "json"  # json, text
    destination: Optional[str] = None  # file path, webhook URL, etc.
    batch_size: int = 100
    flush_interval: int = 30  # seconds
    correlation_enabled: bool = True
    include_traceback: bool = True
    max_buffer_size: int = 1000
    pretty_print: bool = False  # Pretty print JSON for development

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the configuration"""
        raise NotImplementedError()


# hector -- does this make sense, or should it inherit LogConfig and not have a get_cloud_config method?
@dataclass
class ConsoleLogConfig(LogConfig):
    """Console-specific log configuration"""

    def to_platform_config(self) -> Dict[str, Any]:
        return {"provider": "console"}

    def validate_config(self) -> bool:
        return True
