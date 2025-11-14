import json
import sys
from typing import List

from ..client.enums import LogLevel
from ..client.models import LogEntry
from ..color_utils import colorize
from .base import LogHandler

# Default color mapping for log levels
# Using distinct colors with ANSI styles for better visual hierarchy
DEFAULT_LOG_COLORS = {
    LogLevel.DEBUG: "cyan",  # Cyan for debug (less prominent)
    LogLevel.INFO: "bright_green",  # Bright green for info (positive, prominent)
    LogLevel.WARNING: "bright_yellow",  # Bright yellow for warnings (attention)
    LogLevel.ERROR: "bright_red",  # Bright red for errors (urgent)
    LogLevel.CRITICAL: "bold_red",  # Bold red for critical (very urgent)
}


class ConsoleHandler(LogHandler):
    """Handler for console output"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure stdout to use UTF-8 encoding for emoji support
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8")
            except Exception:
                pass  # Silently fail if reconfiguration not supported

    def _get_color_for_entry(self, entry: LogEntry) -> str:
        """Get the color for a log entry, using default if not specified"""
        # If color is explicitly set, use it
        if entry.color:
            return entry.color

        # Otherwise, use default color based on log level
        return DEFAULT_LOG_COLORS.get(entry.level, "green")

    async def write(self, entries: List[LogEntry]) -> bool:
        """Write entries to console"""
        try:
            for entry in entries:
                # Get the color to use (explicit or default)
                color = self._get_color_for_entry(entry)

                if self.config.format == "json":
                    if self.config.pretty_print:
                        # Pretty print JSON for development
                        json_output = json.dumps(entry.to_dict(), indent=2, default=str)
                        # Apply color to the entire JSON output
                        json_output = colorize(json_output, color)
                        print(json_output)
                        print("-" * 80)  # Separator for readability
                    else:
                        json_output = entry.to_json()
                        # Apply color to the entire JSON output
                        json_output = colorize(json_output, color)
                        print(json_output)
                else:
                    # Text format with enhanced colorization

                    # Color different parts of the log line
                    timestamp = colorize(f"[{entry.timestamp}]", "gray")
                    level = colorize(entry.level.value.upper(), color)
                    app_name = colorize(entry.app_name, "blue")

                    log_line = f"{timestamp} {level} {app_name}: {entry.message}"
                    print(log_line)
            return True
        except Exception as e:
            print(f"Error writing to console: {e}")
            raise

    async def flush(self) -> bool:
        """Console output doesn't need flushing"""
        return True
