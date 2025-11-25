#!/usr/bin/env python3
"""
Advanced Logging Example for dc_logger

This script demonstrates advanced dc_logger features:
- Multi-handler configuration (console + file)
- HTTP details logging
- Correlation tracking for distributed tracing
- Multi-tenant context
- Error handling patterns
- Using decorators for automatic logging

Run this example:
    python advanced_logging.py
"""

import asyncio
import os
import tempfile

from dc_logger import (
    DCLogger,
    HTTPDetails,
    LogEntity,
    LogLevel,
    MultiTenant,
    correlation_manager,
    create_console_file_config,
    log_call,
)

# =================================================================
# Decorator Examples
# =================================================================


@log_call(action_name="fetch_user_data", include_params=True)
async def fetch_user_data(user_id: str, include_details: bool = False) -> dict:
    """
    Fetch user data with automatic logging.

    The @log_call decorator automatically logs:
    - Function entry with parameters
    - Function exit with result/error
    - Execution duration
    """
    # Simulate API call
    await asyncio.sleep(0.1)
    return {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "details": {"role": "admin"} if include_details else None,
    }


@log_call(
    action_name="process_payment",
    log_level=LogLevel.INFO,
    include_params=True,
    sensitive_params=["card_number", "cvv"],  # These will be masked
)
async def process_payment(
    order_id: str,
    amount: float,
    card_number: str,
    cvv: str,
) -> dict:
    """
    Process payment with sensitive data masking.

    The sensitive_params list ensures card_number and cvv
    are not logged in plain text.
    """
    await asyncio.sleep(0.05)
    return {"order_id": order_id, "status": "approved", "amount": amount}


async def main() -> None:
    """Demonstrate advanced dc_logger features."""

    print("=" * 60)
    print("DC Logger - Advanced Logging Example")
    print("=" * 60)
    print()

    # =================================================================
    # Multi-Handler Setup (Console + File)
    # =================================================================
    print(">>> Setting up multi-handler logging (console + file)")
    print()

    # Create a temporary log file for this example
    log_dir = tempfile.mkdtemp()
    log_file = os.path.join(log_dir, "advanced_example.log")

    config = create_console_file_config(
        file_path=log_file,
        level=LogLevel.DEBUG,
        pretty_print=True,
    )

    logger = DCLogger(config, app_name="advanced_example")

    print(f"Log file created at: {log_file}")
    print()

    # =================================================================
    # HTTP Details Logging
    # =================================================================
    print(">>> HTTP Details Logging")
    print()

    # Log an API request with full HTTP details
    http_details = HTTPDetails(
        method="POST",
        url="https://api.example.com/v1/datasets/12345/upload",
        status_code=201,
        headers={"Content-Type": "application/json"},
        response_size=4096,
        params={"format": "csv", "overwrite": True},
    )

    await logger.info(
        "API request completed successfully",
        http_details=http_details,
        action="upload_data",
        duration_ms=1250,
    )

    # Log a failed request
    failed_http = HTTPDetails(
        method="GET",
        url="https://api.example.com/v1/users/99999",
        status_code=404,
    )

    await logger.warning(
        "Resource not found",
        http_details=failed_http,
        action="get_user",
    )

    print()

    # =================================================================
    # Correlation Tracking
    # =================================================================
    print(">>> Correlation Tracking (Distributed Tracing)")
    print()

    # Start a new request context
    request_id = correlation_manager.start_request()
    context = correlation_manager.get_current_context()

    await logger.info(
        "Starting distributed operation",
        action="distributed_op",
        extra={
            "request_id": request_id,
            "trace_id": context["trace_id"],
            "span_id": context["span_id"],
        },
    )

    # Simulate calling another service
    # In real code, you'd pass trace_id to the other service
    await asyncio.sleep(0.05)

    # Create a child span
    child_correlation = correlation_manager.get_or_create_correlation()

    await logger.info(
        "Child operation completed",
        action="child_op",
        extra={
            "parent_span_id": child_correlation.parent_span_id,
            "span_id": child_correlation.span_id,
        },
    )

    print()

    # =================================================================
    # Multi-Tenant Logging
    # =================================================================
    print(">>> Multi-Tenant Context")
    print()

    tenant = MultiTenant(
        user_id="user_12345",
        tenant_id="tenant_acme",
        organization_id="org_enterprise",
        session_id="sess_abc123",
    )

    await logger.info(
        "Tenant operation performed",
        multi_tenant=tenant,
        action="update_settings",
        entity=LogEntity(type="settings", id="general", name="General Settings"),
    )

    print()

    # =================================================================
    # Using Decorators
    # =================================================================
    print(">>> Decorator-based Automatic Logging")
    print()

    # These functions are decorated with @log_call
    user_data = await fetch_user_data("usr_123", include_details=True)
    print(f"Fetched user: {user_data['name']}")

    # Payment processing with masked sensitive data
    payment = await process_payment(
        order_id="ord_789",
        amount=99.99,
        card_number="4111111111111111",  # Will be masked in logs
        cvv="123",  # Will be masked in logs
    )
    print(f"Payment status: {payment['status']}")

    print()

    # =================================================================
    # Error Handling Pattern
    # =================================================================
    print(">>> Error Handling Pattern")
    print()

    entity = LogEntity(type="report", id="rpt_001", name="Monthly Sales")

    try:
        await logger.info(
            "Starting report generation",
            entity=entity,
            action="generate_report",
        )

        # Simulate an error
        raise ValueError("Invalid date range specified")

    except ValueError as e:
        await logger.error(
            f"Report generation failed: {e}",
            entity=entity,
            action="generate_report",
            extra={
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
        )
        print(f"Caught and logged error: {e}")

    print()

    # =================================================================
    # Cleanup
    # =================================================================
    print(">>> Closing logger and showing log file contents")
    await logger.close()

    # Show the log file contents
    print()
    print("-" * 40)
    print("Contents of log file:")
    print("-" * 40)
    with open(log_file) as f:
        print(f.read())

    print("=" * 60)
    print("Advanced example completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
