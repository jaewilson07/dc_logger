import datetime as dt
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
import json

from .enums import LogLevel


@dataclass
class Entity:
    """Entity information for logging"""

    type: str  # dataset, card, user, dataflow, page, etc.
    id: Optional[str] = None
    name: Optional[str] = None
    additional_info: Dict[str, Any] = field(default_factory=dict)
    parent: Any = None  # instance of a class

    def get_additional_info(self, info_fn: Callable = None):
        if info_fn:
            self.additional_info = info_fn(self)
            return self.additional_info

        additional_info = {}
        if hasattr(self.parent, "description"):
            additional_info["description"] = getattr(self.parent, "description", "")
        if hasattr(self.parent, "owner"):
            additional_info["owner"] = getattr(self.parent, "owner", {})
        if hasattr(self.parent, "display_type"):
            additional_info["display_type"] = getattr(self.parent, "display_type", "")
        if hasattr(self.parent, "data_provider_type"):
            additional_info["data_provider_type"] = getattr(
                self.parent, "data_provider_type", ""
            )

        # Get auth instance info
        if hasattr(self.parent, "auth") and self.parent.auth:
            additional_info["domo_instance"] = getattr(
                self.parent.auth, "domo_instance", None
            )

        self.additional_info = additional_info
        return self.additional_info

    @classmethod
    def from_domo_entity(cls, domo_entity, info_fn: Callable = None) -> "Entity":
        """Create Entity from a DomoEntity object"""

        if not domo_entity:
            return None

        # Extract entity type from class name (e.g., DomoDataset -> dataset)
        entity_type = cls._extract_entity_type(type(domo_entity).__name__)

        entity = cls(
            type=entity_type,
            parent=domo_entity,
            id=getattr(domo_entity, "id", None),
            name=getattr(domo_entity, "name", None),
        )
        entity.get_additional_info(info_fn=info_fn)

        return entity

    @staticmethod
    def _extract_entity_type(class_name: str) -> str:
        """Extract entity type from DomoEntity class name"""
        # Remove 'Domo' prefix and convert to lowercase
        if class_name.startswith("Domo"):
            return class_name[4:].lower()
        return class_name.lower()


@dataclass
class HTTPDetails:
    """HTTP request/response details"""

    method: Optional[str] = None
    url: Optional[str] = None
    status_code: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    response_size: Optional[int] = None
    request_body: Optional[Any] = None
    response_body: Optional[Any] = None


@dataclass
class Correlation:
    """Correlation information for distributed tracing"""

    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    parent_span_id: Optional[str] = None


@dataclass
class MultiTenant:
    """Multi-tenant information"""

    user_id: Optional[str] = None
    session_id: Optional[str] = None
    tenant_id: Optional[str] = None
    organization_id: Optional[str] = None


@dataclass
class LogEntry:
    """Enhanced log entry with structured JSON format"""

    # Core log fields
    timestamp: str
    level: LogLevel
    logger: str
    message: str

    # Business context
    user: Optional[str] = None
    action: Optional[str] = None
    entity: Optional[Entity] = None
    status: str = "info"
    duration_ms: Optional[int] = None

    # Distributed tracing
    correlation: Optional[Correlation] = None

    # Multi-tenant context
    multi_tenant: Optional[MultiTenant] = None

    # HTTP details (for API calls)
    http_details: Optional[HTTPDetails] = None

    # Flexible metadata
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            # Core log fields
            "timestamp": self.timestamp,
            "level": self.level.value,
            "logger": self.logger,
            "message": self.message,
            # Business context
            "user": self.user
            or (
                self.multi_tenant.user_id
                if self.multi_tenant and self.multi_tenant.user_id
                else None
            ),
            "action": self.action,
            "status": self.status,
            "duration_ms": self.duration_ms,
            # Entity (serialize if present)
            "entity": self.entity.__dict__ if self.entity else None,
            # Correlation (serialize if present)
            "correlation": self.correlation.__dict__ if self.correlation else None,
            # Multi-tenant (serialize if present)
            "multi_tenant": self.multi_tenant.__dict__ if self.multi_tenant else None,
            # HTTP details (serialize if present and has data)
            "http_details": self._serialize_http_details(),
            # Flexible metadata
            "extra": self.extra,
        }

        # Remove None values for cleaner output
        return {k: v for k, v in result.items() if v is not None}

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def create(cls, level: LogLevel, message: str, logger: str, **kwargs) -> "LogEntry":
        """Factory method to create a LogEntry with current timestamp"""
        timestamp = dt.datetime.utcnow().isoformat() + "Z"

        # Extract known fields
        user = kwargs.get("user")
        action = kwargs.get("action")
        status = kwargs.get("status", "info")
        duration_ms = kwargs.get("duration_ms")
        extra = kwargs.get("extra", {})

        # Handle entity - could be dict, Entity object, or DomoEntity object
        entity = kwargs.get("entity")
        if isinstance(entity, dict) and entity:
            entity_obj = Entity(**entity)
        elif isinstance(entity, Entity):
            entity_obj = entity
        elif entity and hasattr(entity, "id"):  # DomoEntity object
            entity_obj = Entity.from_domo_entity(entity)
        else:
            entity_obj = None

        # Handle correlation - could be dict, Correlation object, or individual fields
        correlation_obj = None
        correlation = kwargs.get("correlation")
        if isinstance(correlation, dict) and correlation:
            correlation_obj = Correlation(**correlation)
        elif isinstance(correlation, Correlation):
            correlation_obj = correlation
        elif any(k in kwargs for k in ["trace_id", "span_id", "parent_span_id"]):
            # Create correlation from individual fields
            correlation_obj = Correlation(
                trace_id=kwargs.get("trace_id"),
                span_id=kwargs.get("span_id"),
                parent_span_id=kwargs.get("parent_span_id"),
            )

        # Handle multi-tenant - could be dict, MultiTenant object, or individual fields
        multi_tenant_obj = None
        multi_tenant = kwargs.get("multi_tenant")
        if isinstance(multi_tenant, dict) and multi_tenant:
            multi_tenant_obj = MultiTenant(**multi_tenant)
        elif isinstance(multi_tenant, MultiTenant):
            multi_tenant_obj = multi_tenant
        elif any(
            k in kwargs
            for k in ["user_id", "session_id", "tenant_id", "organization_id"]
        ):
            # Create multi-tenant from individual fields
            multi_tenant_obj = MultiTenant(
                user_id=kwargs.get("user_id") or kwargs.get("user"),
                session_id=kwargs.get("session_id"),
                tenant_id=kwargs.get("tenant_id"),
                organization_id=kwargs.get("organization_id"),
            )

        # Handle HTTP details - could be dict, HTTPDetails object, or individual fields
        http_details_obj = None
        http_details = kwargs.get("http_details")
        if isinstance(http_details, dict) and http_details:
            http_details_obj = HTTPDetails(**http_details)
        elif isinstance(http_details, HTTPDetails):
            http_details_obj = http_details
        elif any(
            k in kwargs
            for k in ["method", "url", "status_code", "headers", "response_size"]
        ):
            # Create HTTP details from individual fields
            http_details_obj = HTTPDetails(
                method=kwargs.get("method"),
                url=kwargs.get("url"),
                status_code=kwargs.get("status_code"),
                headers=kwargs.get("headers"),
                response_size=kwargs.get("response_size"),
                request_body=kwargs.get("request_body"),
                response_body=kwargs.get("response_body"),
            )

        # If user is not set but multi_tenant has user_id, use that
        if not user and multi_tenant_obj and multi_tenant_obj.user_id:
            user = multi_tenant_obj.user_id

        return cls(
            timestamp=timestamp,
            level=level,
            logger=logger,
            message=message,
            user=user,
            action=action,
            entity=entity_obj,
            status=status,
            duration_ms=duration_ms,
            correlation=correlation_obj,
            multi_tenant=multi_tenant_obj,
            http_details=http_details_obj,
            extra=extra,
        )

    def _serialize_http_details(self) -> Optional[Dict[str, Any]]:
        """Serialize HTTP details for logging, filtering sensitive data"""
        if not self.http_details:
            return None

        http_details_dict = {}

        if self.http_details.method:
            http_details_dict["method"] = self.http_details.method

        if self.http_details.url:
            http_details_dict["url"] = self.http_details.url

        if self.http_details.headers:
            # Only include important headers, not sensitive ones
            safe_headers = {}
            for k, v in self.http_details.headers.items():
                if k.lower() not in [
                    "authorization",
                    "cookie",
                    "x-domo-authentication",
                ]:
                    safe_headers[k] = v
            if safe_headers:
                http_details_dict["headers"] = safe_headers

        if self.http_details.params:
            http_details_dict["params"] = self.http_details.params

        if self.http_details.request_body:
            # Truncate large request bodies
            if (
                isinstance(self.http_details.request_body, str)
                and len(self.http_details.request_body) > 500
            ):
                http_details_dict["request_body"] = (
                    self.http_details.request_body[:500] + "..."
                )
            else:
                http_details_dict["request_body"] = self.http_details.request_body

        if self.http_details.response_body:
            # Truncate large response bodies
            if (
                isinstance(self.http_details.response_body, str)
                and len(self.http_details.response_body) > 500
            ):
                http_details_dict["response_body"] = (
                    self.http_details.response_body[:500] + "..."
                )
            else:
                http_details_dict["response_body"] = self.http_details.response_body

        return http_details_dict if http_details_dict else None
