from typing import List

from .base import CloudHandler
from ...client.models import LogEntry

#| export


@dataclass
class AWSCloudWatch_ServiceConfig(CloudServiceConfig):
    """AWS CloudWatch-specific log configuration"""
    output_mode: OutputMode = "cloud"
    cloud_provider: str = "aws"
    
    aws_region: str = ""
    log_group: str = ""

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


class AWSCloudWatchHandler(CloudHandler):
    """AWS CloudWatch log handler"""

    async def _send_to_cloud(self, entries: List[LogEntry]) -> bool:
        """Send log entries to AWS CloudWatch"""
        # TODO: Implement AWS CloudWatch integration using boto3

        print(f"AWS CloudWatch: Would send {len(entries)} log entries")
        return True