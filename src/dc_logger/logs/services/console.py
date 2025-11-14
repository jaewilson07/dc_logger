__all__ = ["ConsoleServiceConfig", "ConsoleHandler"]


import json
import sys
from dataclasses import dataclass
from typing import List

from dc_logger.client.base import LogEntry, OutputMode, ServiceConfig, ServiceHandler


@dataclass
class ConsoleServiceConfig(ServiceConfig):
    """Console-specific log configuration"""

    output_mode: OutputMode = "console"
    format: str = "text"

    def validate_config(self) -> bool:
        return True


class ConsoleHandler(ServiceHandler):
    """Handler for console output"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure stdout to use UTF-8 encoding for emoji support
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8")
            except Exception:
                pass  # Silently fail if reconfiguration not supported

    async def _write_json(self, entry: LogEntry) -> bool:
        message = json.dumps(entry.to_dict(), indent=2, default=str)
        print(message)
        return True

    async def _write_text(self, entry: LogEntry) -> bool:
        message = (
            f"[{entry.timestamp}] {entry.level.value} {entry.app_name}: {entry.message}"
        )
        print(message)
        return True

    async def write(self, entries: List[LogEntry]) -> bool:
        """Write entries to console"""
        try:
            for entry in entries:
                if (
                    self.service_config
                    and hasattr(self.service_config, "format")
                    and self.service_config.format == "json"
                ):
                    await self._write_json(entry)
                else:
                    await self._write_text(entry)
            return True
        except Exception as e:
            print(f"Error writing to console: {e}")
            raise

    async def flush(self) -> bool:
        """Console output doesn't need flushing"""
        return True
