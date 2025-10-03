from typing import List
from abc import abstractmethod

from ...client.models import LogEntry
from ...client.exceptions import LogWriteError
from ..base import LogHandler

#| export




@dataclass
class Logger(LogConfig):
    """Configuration that supports multiple handlers simultaneously"""
    handlers: List[HandlerConfig] = field(default_factory=list)
    
    output_mode: str = "multi"
    
    def get_cloud_config(self) -> Dict[str, Any]:
        return {"cloud_provider": "multi"}
    
    def validate_config(self) -> bool:
        for handler in self.handlers:
            if not handler.config.validate_config():
                return False
        return True
    
    def get_handler_configs(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": handler.type,
                "config": handler.config,
                "cloud_config": (
                    handler.config.to_platform_config()
                    if handler.type == "cloud"
                    else None
                ),
            }
            for handler in self.handlers
        ]
    
    @classmethod
    def create(
        cls,
        handlers: List[Dict[str, Any]],
        level: LogLevel = LogLevel.INFO,
        batch_size: int = 100,
        flush_interval: int = 30,
        **kwargs
    ) -> "MultiHandlerLogConfig":
        handler_configs = [
            HandlerConfig(type=h["type"], config=h["config"]) for h in handlers
        ]
        return cls(
            handlers=handler_configs,
            level=level,
            batch_size=batch_size,
            flush_interval=flush_interval,
            **kwargs
        )
    

class CloudHandler(LogHandler):
    """Base class for cloud log handlers"""

    def __init__(self, config):
        super().__init__(config)
        self.cloud_config = config.to_platform_config()
        config.validate_config()

    @abstractmethod
    async def _send_to_cloud(self, entries: List[LogEntry]) -> bool:
        """Send entries to cloud provider"""
        pass

    async def write(self, entries: List[LogEntry]) -> bool:
        """Write entries to cloud provider"""
        try:
            return await self._send_to_cloud(entries)
        except Exception as e:
            raise LogWriteError(f"Error sending logs to cloud provider: {e}")

    async def flush(self) -> bool:
        """Cloud handlers may need batching, implement in subclasses"""
        return True
