import asyncio
import socket
from typing import List
import concurrent.futures

from .base import CloudHandler
from ...client.models import LogEntry
from ...client.enums import LogLevel
from ...client.exceptions import LogHandlerError


class DatadogHandler(CloudHandler):
    """Datadog log handler using direct HTTP API"""

    def __init__(self, config):
        super().__init__(config)
        self._validate_config()

    def _validate_config(self):
        """Validate Datadog configuration"""
        api_key = self.cloud_config.get("api_key")
        if not api_key:
            raise LogHandlerError("Datadog API key is required")

    def _get_hostname(self) -> str:
        """Get the actual hostname/IP address of the machine"""
        try:
            # Try to get the hostname, fallback to IP if needed
            hostname = socket.gethostname()
            # Get the IP address for more specific identification
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except:
            # Fallback to localhost if hostname resolution fails
            return "127.0.0.1"

    def _convert_log_level(self, level: LogLevel) -> str:
        """Convert LogLevel enum to Datadog log level"""
        level_mapping = {
            LogLevel.DEBUG: "debug",
            LogLevel.INFO: "info",
            LogLevel.WARNING: "warning",
            LogLevel.ERROR: "error",
            LogLevel.CRITICAL: "critical",
        }
        return level_mapping.get(level, "info")

    def _send_logs_simple_api(self, entries: List[LogEntry]) -> bool:
        """Send logs using direct HTTP requests to Datadog"""
        try:
            import requests

            # Get configuration
            api_key = self.cloud_config.get("api_key")
            site = self.cloud_config.get("site", "datadoghq.com")

            # Determine the intake URL based on site
            if site == "datadoghq.com":
                intake_url = "https://http-intake.logs.datadoghq.com/v1/input"
            elif site.startswith("us"):
                region = site.replace(".datadoghq.com", "")
                intake_url = f"https://http-intake.logs.{region}.datadoghq.com/v1/input"
            else:
                intake_url = f"https://http-intake.logs.{site}/v1/input"

            # Convert entries to log format
            logs_data = []
            hostname = self._get_hostname()
            for entry in entries:
                log_data = {
                    "message": entry.message,
                    "ddsource": "domolibrary",
                    "service": self.cloud_config.get("service", "domolibrary"),
                    "hostname": hostname,
                    "status": self._convert_log_level(entry.level),
                    "ddtags": f"env:{self.cloud_config.get('env', 'production')},service:{self.cloud_config.get('service', 'domolibrary')}",
                    "timestamp": entry.timestamp,
                }

                # Add structured data
                if entry.entity:
                    log_data["entity"] = entry.entity.__dict__

                if entry.correlation:
                    log_data["correlation"] = {
                        "trace_id": entry.correlation.trace_id,
                        "span_id": entry.correlation.span_id,
                        "parent_span_id": entry.correlation.parent_span_id,
                    }

                if entry.multi_tenant:
                    log_data["multi_tenant"] = {
                        "user_id": entry.multi_tenant.user_id,
                        "session_id": entry.multi_tenant.session_id,
                        "tenant_id": entry.multi_tenant.tenant_id,
                        "organization_id": entry.multi_tenant.organization_id,
                    }

                if entry.http_details:
                    log_data["http_details"] = {
                        "method": entry.http_details.method,
                        "url": entry.http_details.url,
                        "status_code": entry.http_details.status_code,
                    }

                if entry.extra:
                    log_data.update(entry.extra)

                logs_data.append(log_data)

            # Send via HTTP POST
            headers = {"Content-Type": "application/json", "DD-API-KEY": api_key}

            response = requests.post(
                intake_url, json=logs_data, headers=headers, timeout=10
            )

            if response.status_code in [200, 202]:
                return True
            else:
                print(
                    f"DatadogHandler: Failed to send logs - Status {response.status_code}: {response.text}"
                )
                return False

        except Exception as e:
            print(f"DatadogHandler: Failed to send logs - {e}")
            return False

    async def _send_to_cloud(self, entries: List[LogEntry]) -> bool:
        """Send log entries to Datadog using direct HTTP API"""

        def submit_logs():
            return self._send_logs_simple_api(entries)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(submit_logs)
            result = await asyncio.wrap_future(future)
            return result
