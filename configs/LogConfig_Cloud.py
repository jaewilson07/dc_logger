import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from abc import abstractmethod
from .LogConfig import LogConfig, OutputMode
from ..client.exceptions import LogConfigError


@dataclass
class LogCloudConfig(LogConfig):

    @abstractmethod
    def to_platform_config(self) -> Dict[str, Any]:
        """Get cloud provider specific configuration"""
        raise NotImplementedError()


@dataclass
class DatadogLogConfig(LogConfig):
    """Datadog-specific log configuration"""

    api_key: Optional[str] = field(repr=False)
    app_key: Optional[str] = field(repr=False)

    cloud_provider: str = "datadog"
    output_mode: OutputMode = "cloud"

    site: str = "datadoghq.com"
    service: str = "domolibrary"
    env: str = "production"

    def to_platform_config(self) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "app_key": self.app_key,
            "site": self.site,
            "service": self.service,
            "env": self.env,
            "cloud_provider": self.cloud_provider,
        }

    def validate_config(self) -> bool:
        if not self.api_key:
            raise LogConfigError("Datadog API key is required")
        return True


@dataclass
class AWSCloudWatchLogConfig(LogConfig):
    """AWS CloudWatch-specific log configuration"""

    aws_region: str
    log_group: str

    cloud_provider: str = "aws"
    output_mode: OutputMode = "cloud"

    log_stream: Optional[str] = None

    def to_platform_config(self) -> Dict[str, Any]:
        return {
            "aws_region": self.aws_region,
            "log_group": self.log_group,
            "log_stream": self.log_stream,
            "cloud_provider": self.cloud_provider,
        }

    def validate_config(self) -> bool:
        if not self.aws_region:
            raise LogConfigError("AWS region is required")
        if not self.log_group:
            raise LogConfigError("AWS log group is required")
        return True


@dataclass
class GCPLoggingConfig(LogConfig):
    """Google Cloud Logging-specific configuration"""

    log_name: str

    project_id: Optional[str] = None

    output_mode: OutputMode = "cloud"
    cloud_provider: str = "gcp"

    def to_cloud_config(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "log_name": self.log_name,
            "cloud_provider": self.cloud_provider,
        }

    def validate_config(self) -> bool:
        if not self.project_id:
            raise LogConfigError("GCP project ID is required")
        return True


@dataclass
class AzureLogAnalyticsConfig(LogConfig):
    """Azure Log Analytics-specific configuration"""

    workspace_id: Optional[str] = field(
        default_factory=lambda: os.getenv("AZURE_WORKSPACE_ID")
    )
    shared_key: Optional[str] = field(
        default_factory=lambda: os.getenv("AZURE_SHARED_KEY")
    )
    log_type: str = "domolibrary"
    output_mode: str = field(default="cloud", init=False)
    cloud_provider: str = field(default="azure", init=False)

    def to_cloud_config(self) -> Dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "shared_key": self.shared_key,
            "log_type": self.log_type,
            "cloud_provider": self.cloud_provider,
        }

    def validate_config(self) -> bool:
        if not self.workspace_id:
            raise LogConfigError("Azure workspace ID is required")
        if not self.shared_key:
            raise LogConfigError("Azure shared key is required")
        return True
