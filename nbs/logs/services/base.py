from typing import List
from abc import ABC, abstractmethod

from ..configs.base import LogConfig
from ..client.models import LogEntry



#| export


@dataclass
class HandlerConfig:
    type: str
    config: LogConfig
    platform_config: Optional[Dict[str, Any]] = None

    @classmethod
    def from_config(cls, config: LogConfig):
        hc = cls(
            type=config.output_mode,
            config=config,
        )
        if hasattr(config, 'to_platform_config') and callable(getattr(config, 'to_platform_config')):
            hc.platform_config = config.to_platform_config()
        return hc


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